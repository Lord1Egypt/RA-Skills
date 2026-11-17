# Szczegóły procesu rejestracji — powpow-register

Materiał do podglądu przy rozwiązywaniu problemów. Wszystkie reguły pochodzą z kodu platformy (spójna
walidacja frontend-backend w Next.js), ze wskazaniem źródeł. Przy aktualizacji platformy obowiązuje
rzeczywiste zachowanie na produkcji.

## Punkty wejścia

- Strona rejestracji: https://global.powpow.online/register
- Strona logowania: https://global.powpow.online/login
- Strona subskrypcji: https://global.powpow.online/subscription
- Wejście z linku udostępnienia itp. z `?next=...`: po rejestracji + płatności następuje automatyczny powrót
  na pierwotną stronę.

## Pola formularza i reguły

| Pole | Wymagane | Reguła | Źródło w kodzie |
|---|---|---|---|
| Avatar | opcjonalne | Obrazek ≤5MB, SVG niewspierane; serwer kompresuje automatycznie (przy >100KB do 400×400 / jakość 90) | `src/app/api/auth/register/route.ts` |
| Nazwa użytkownika | wymagane | 2~50 znaków; po trim zapisywane **małymi literami** (Tom i tom to ta sama nazwa; rejestracja i logowanie ignorują wielkość liter) | jw. (zod schema) |
| Hasło | wymagane | 8~100 znaków; musi naraz zawierać wielką literę, małą literę i cyfrę | jw. |
| Potwierdzenie hasła | wymagane | Zgodne z hasłem (tylko walidacja frontendu) | `src/app/(public)/register/page.tsx` |
| Pseudonim | opcjonalne | ≤100 znaków; puste → domyślnie nazwa użytkownika | register route |
| E-mail | **wymagane** | Poprawny format e-mail, ≤255 znaków; jeden e-mail może zarejestrować tylko jedno konto | register route |
| Kod weryfikacyjny e-mail | **wymagane** | 6 cyfr; **ważny 10 minut**; po udanej weryfikacji przepada; ponowna wysyłka oznacza stary kod jako użyty | `src/lib/email-verification.ts` |
| Numer telefonu | opcjonalne | Numer z Chin kontynentalnych: 11 cyfer zaczynających się od `1[3-9]`; jeden numer można powiązać tylko z jednym kontem | register route |

Strona ma też trzy przyciski logowania przez osoby trzecie: **Google, Watcha, konto Huawei**
(`GoogleSignInButton` / `WatchaLoginButton` / `HuaweiLoginButton`). Konta z osób trzecich nie mają lokalnego
hasła — późniejsza próba logowania hasłem zwróci 「该账号未设置密码，请使用其他方式登录」 (to konto nie ma
ustawionego hasła, zaloguj się innym sposobem).

## Limity i parametry ochrony przed brute force

| Czynność | Limit | Źródło |
|---|---|---|
| Zgłoszenie rejestracji | **3 razy/min/IP**, ponad limit 429 | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Wysyłka kodu weryfikacyjnego | Ten sam IP 1 raz/min **i** ten sam e-mail 1 raz/min, ponad limit 429; przycisk frontendu z 60-sekundowym odliczaniem | `src/app/api/auth/register/send-code/route.ts` |
| Walidacja kodu | Na e-mail maks. **5 prób** w 10 minut; po osiągnięciu limitu nawet poprawny kod jest odrzucany — trzeba wysłać nowy | `src/lib/email-verification.ts` |
| Kod przy „nie pamiętam hasła" | 1 raz/min/IP | `src/app/api/auth/forgot-password/route.ts` |
| Logowanie | 5 razy/min/IP; to samo konto po **5 nieudanych próbach z rzędu blokada 30 minut** (423), w tym czasie licznik pozostałych prób maleje | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Ochrona prywatności**: przy wysyłce kodu / odzyskiwaniu hasła, jeśli e-mail jest już zajęty albo nie
istnieje, interfejs i tak zwraca komunikat sukcesu — nie zdradza, czy e-mail jest zarejestrowany.

## Równoważność trybu agenta i rejestracji przez www

Skrypt skilla woła **ten sam zestaw publicznych API** (`/api/auth/register`, `send-code`, `login`,
`/api/auth/me`) i przechodzi dokładnie tę samą ścieżkę walidacji, limitów i błędów co formularz na stronie
rejestracji — wszystkie reguły z tego pliku obowiązują identycznie w obu trybach. Sekwencję i kontrakt poleceń
skryptu opisuje `references/agent-flow.md`.

## Przebieg statusów po udanej rejestracji

> **Bezpłatny okres testowy (od 2026-10-18; faktyczne zachowanie platformy ma pierwszeństwo)**: nowe zarejestrowane konto może **korzystać ze wszystkich funkcji od razu**
> (feed, mapa, cyfrowi ludzie, odznaki itd.) bez żadnej płatności; konta bez subskrypcji nie są już odcinane od stron treści. Opisane tutaj
> „przechwytywanie pending” to regularny stan po zakończeniu okresu testowego — kiedy to nadejdzie, pierwszeństwo ma faktyczne zachowanie online.

1. Użytkownik jest zapisany z `accountStatus: 'pending'` i **3 startowymi odznakami** (trasa register).
2. Serwer sadzi też dwa ciasteczka HttpOnly: JWT (można wchodzić na strony od razu) i pendingUserToken (poświadczenie tożsamości dla przepływu subskrypcji).
3. W stanie regularnym (okres testowy skończony / brak okresu bezpłatnego) strona rejestracji wykrywa `pending_payment` → przekierowanie na `/subscription`
   (z zachowaniem parametru powrotu `next`); w trybie pośrednictwa agenta `me?token=…&redirect=/subscription` daje ten sam efekt.
   **W bezpłatnym okresie testowym ten krok nie wyzwala się** — po rejestracji idź od razu na stronę główną i zacznij korzystać.
4. Płatność zakończona → `accountStatus` staje się `active` (**Alipay aktywuje automatycznie po stronie serwera przez notify**;
   PayPal aktywuje przez Webhook; kod QR WeChat potwierdzany ręcznie; Huawei IAP przechodzi przez `activate-huawei`).
   Szczegóły w `payment-and-activation.md`.

W stanie regularnym nieaktywne (pending) konta wywołujące kluczowe API (feed, mapa, czat z cyfrowymi ludźmi, odznaki itd.) dostają 403;
wyjątek to udostępnione linki do postów (zostają publicznie dostępne). W bezpłatnym okresie testowym to przechwytywanie jest zawieszone i wszystko jest otwarte.
## Tabela typowych błędów

| Objaw | Przyczyna | Co robić |
|---|---|---|
| 「用户名已存在」 (nazwa użytkownika już istnieje) | Nazwa zajęta (wielkość liter bez znaczenia) | Wybierz inną nazwę |
| 「邮箱已被使用」 (e-mail już używany) | E-mail był już rejestrowany | Inny e-mail; albo jednak logowanie + „nie pamiętam hasła" po stare konto |
| 「邮箱验证码错误或已过期」 (kod weryfikacyjny błędny lub wygasł) | Literówka w kodzie / ponad 10 minut / odrzucenie po ponad 5 błędnych próbach | Kliknij „wyślij ponownie" i użyj kodu z **najnowszego** maila |
| Kod nie dochodzi | Limit 60 sekund; albo mail wpadł do spamu/ofert | Odczekaj koniec odliczania i wyślij ponownie; przejrzyj folder spam |
| 「手机号已被使用」 (numer telefonu już używany) | Numer jest już przypisany do innego konta | Usuń numer telefonu (pole opcjonalne) albo podaj inny |
| 「注册请求过于频繁」 (zbyt częste zgłoszenia rejestracji) / 429 | Osiągnięty limit 3 zgłoszeń/min/IP | Odczekaj kilka minut i ponów |
| 409 「用户名或邮箱已被注册」 (nazwa użytkownika lub e-mail już zarejestrowany) | Kolizja nazwy z kimś w chwili zgłoszenia (zabezpieczenie na współbieżność) | Zmień nazwę lub e-mail i ponów |
| 「图片大小不能超过5MB」 (obrazek nie może przekraczać 5MB) / 「不支持 SVG」 (SVG niewspierane) | Avatar niezgodny z regułami | Zmień obrazek albo pomiń avatar |
| Użytkownik klika link logowania, ale trafia na stronę subskrypcji (zamiast strony głównej) | Bezpłatny okres testowy się skończył, paywall platformy wrócił | Kieruj się przepływem subskrypcji z kroku 7 w SKILL.md; po subskrypcji uruchom `refresh-login`, potem wyślij link do strony głównej |
| Rejestracja przeszła, ale logowanie zwraca 403 „请完成订阅以激活账户” | Konto wciąż pending, a platforma nie jest w bezpłatnym okresie testowym (oczekiwany stan przed płatnością) | W bezpłatnym okresie testowym się nie zdarzy; jeśli się zdarzy — okres testowy się skończył, najpierw dokończ subskrypcję; jeśli po płatności nadal 403 — użyto starego JWT, w trybie skryptu uruchom najpierw `refresh-login`, żeby wymienić na świeży stan logowania |
| Logowanie 423 「账户已锁定」 (konto zablokowane) | 5 błędnych haseł z rzędu | Odczekaj 30 minut |
| Logowanie 401 「还剩 N 次尝试机会」 (zostało N prób) | Błędne hasło, blisko blokady | Przemyśl i spróbuj albo od razu „nie pamiętam hasła" |
| 「该账号未设置密码，请使用其他方式登录」 (to konto nie ma ustawionego hasła, zaloguj się innym sposobem) | Konto z osoby trzeciej (Google/Watcha/Huawei) | Zaloguj się pierwotnym przyciskiem zewnętrznym |
| 「该账号已注销」 (to konto zostało wyrejestrowane) | Konto dezaktywowane | Trzeba zarejestrować się ponownie |

## Drobna wiedza o logowaniu (przy okazji rozwiązywania problemów)

Logowanie przyjmuje **nazwę użytkownika / e-mail / numer telefonu** zamiennie (każde z trzech może służyć
jako identyfikator konta).
Nie pamiętasz hasła: strona logowania → „nie pamiętam hasła" → podaj e-mail z rejestracji, odbierz
6-cyfrowy kod → ustaw nowe.
