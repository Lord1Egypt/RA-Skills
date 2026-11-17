---
name: powpow-register
description: Pomaga użytkownikowi w pełni zrealizować rejestrację w PowPow (Bubble) i logowanie jednym kliknięciem bezpośrednio w rozmowie. Agent wypełnia formularz w jego imieniu (w tym przesyła awatar) i wysyła kod weryfikacyjny na e-mail; użytkownik podaje tylko podstawowe dane i sprawdza kod weryfikacyjny raz — nie opuszczając rozmowy. Platforma jest obecnie w bezpłatnym okresie testowym: zarejestrowane konto od razu korzysta ze wszystkich funkcji; płatność subskrypcyjna (Alipay/PayPal) to opcjonalne rozszerzenie członkostwa, które agent też może przeprowadzić wraz z tworzeniem zamówienia i śledzeniem wpływu. Uruchamia się, gdy użytkownik mówi „zarejestruj się w Bubble”, „załóż konto powpow”, „jak się zarejestrować w Bubble”, „pomóż mi założyć konto powpow”, „sign up powpow”; zajmuje się też problemami rejestracji (nie dotarł kod weryfikacyjny, nazwa użytkownika/e-mail zajęte) i aktywacji (logowanie mówi „konto nieaktywowane” / pending_payment, jak subskrybować/płacić, czy Bubble jest darmowy/płatny). Wymaga Node ≥ 18; przy braku automatyczny powrót do trybu czystych wskazówek. Nie obejmuje publikowania/tworzenia cyfrowych ludzi (to zadanie powpow-simple), ani rozwoju kodu.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (asystent rejestracji w Bańce)

Prowadzi nowego użytkownika od „nie wiem, czym jest Bubble” do „zalogowany jednym kliknięciem, gotowy do zabawy” — całość w rozmowie. Użytkownik opuszcza rozmowę tylko raz: **żeby sprawdzić kod weryfikacyjny w skrzynce**. Platforma jest obecnie w bezpłatnym okresie testowym: po rejestracji wszystkie funkcje działają, płatność niepotrzebna; płatność subskrypcyjna to opcjonalne rozszerzenie członkostwa (agent otwiera też kasę i śledzi wpływ).

**Wersja 2.2.0** · 2026-10-18 (od v2 tryb pośrednictwa agenta: kontrakt skryptu i pełna sekwencja w `references/agent-flow.md`; reguły pól, limity i diagnozowanie błędów w `references/registration-flow.md`; kanały płatności w `references/payment-and-activation.md`; lista zrzutów produktu w `references/screenshots.md`. Od v2.1.0 agent może prowadzić też subskrypcje PayPal — obok Alipay. Od v2.2.0 platforma weszła w bezpłatny okres testowy: rejestracja i logowanie jednym kliknięciem wystarczą, żeby korzystać; płatność stała się opcjonalnym upgradem — jeśli użytkownik otworzy link i trafi na stronę subskrypcji, okres testowy się skończył, kieruj się przepływem płatności z kroku 7; przepływ adaptuje się sam, zmiana skryptu niepotrzebna)

## Środowisko uruchomieniowe

- Skrypt główny `scripts/powpow-register.mjs`: **zero zależności**, wymaga **Node ≥ 18**. Przed startem uruchom raz `node scripts/powpow-register.mjs status`, żeby potwierdzić, że środowisko działa.
- Wszystkie zapytania skryptu idą wyłącznie do oficjalnej domeny `https://global.powpow.online`.
- **Brak Node / błędy skryptu**: automatyczny powrót do trybu czystych wskazówek — podaj użytkownikowi stronę rejestracji https://global.powpow.online/register i prowadź go wg `references/registration-flow.md` (w bezpłatnym okresie testowym rejestracja przez stronę jest równie natychmiastowa). Nie wciskaj skryptu w kółko.
- Wznowienie po przerwaniu rozmowy: najpierw `status`, żeby zobaczyć, na którym kroku utknęło, potem idź dalej.

## Trigger Conditions

- Zamiar rejestracji: „zarejestruj Bańkę", „załóż konto powpow", „jak się rejestruje w Bańce", „sign up powpow"
- Rejestracja utknęła: „kod weryfikacyjny nie dochodzi", „mówi, że nazwa użytkownika już istnieje", „hasło ciągle odrzucane"
- Problemy po rejestracji: „logowanie mówi, że konto nie jest aktywowane”, „403 pending_payment”, „jak zapłacić za Bubble / subskrybować”, „czy Bubble jest darmowe/płatne”

**Nie wyzwala się dla**: publikowania postów/tworzenia cyfrowych ludzi (→ powpow-simple); developmentu kodu po stronie Web (osobny skill deweloperski). Gdy użytkownik chce się rejestrować i od razu publikować: najpierw dokończ ten skill, po aktywacji przekaż do powpow-simple.

## Przegląd procesu

| Krok | Co robi agent | Co robi użytkownik |
|---|---|---|
| 1 Prezentacja produktu | Przedstawia + wysyła zrzuty | Rzuca okiem |
| 2 Potwierdzenie danych | Proaktywnie proponuje nazwę użytkownika/pseudonim, hasło z dwóch wariantów, pyta o e-mail | Potwierdza, podaje dane |
| 3 Wysyłka kodu | `send-code` | —— |
| 4 Odczyt kodu | —— | Wchodzi do skrzynki, odczytuje 6-cyfrowy kod, odsyła go |
| 5 Zgłoszenie rejestracji | `register` (z bezpośrednim wgraniem avatara), błędy obsługuje automatycznie | —— |
| 6 Logowanie jednym kliknięciem | `login-link(home)` wprost na stronę główną; jeśli trafi na stronę subskrypcji — krok 7 | Kliknąć link i zacząć |
| 7 Upgrade subskrypcji (opcjonalnie) | Tylko gdy użytkownik chce członkostwa / bezpłatny okres się skończył: prowadzimy pełny przepływ płatności | Wybrać metodę, zapłacić |
| 8 Zamknięcie | `cleanup` + przekazanie danych konta + wprowadzenie do zabawy + polecenie wtyczki | Zaczyna zabawę |

## Krok 1: prezentacja produktu + zrzuty ekranu (nie pomijać)

Większość użytkowników nigdy nie widziała Bańki. Pierwsza rzecz to nie opowiadanie o procesie, tylko sprawienie, żeby produkt **zobaczyli**:

1. Przedstaw Bańkę w ~120 znakach: zamień przypadkowe zdjęcia w dziennik z podróży i przypnij go na publicznej mapie jako „bańkę"; bańka z czasem blaknie, czyjeś polubienie może ją wskrzesić; na mapie są też „cyfrowi ludzie", z którymi można rozmawiać. Adres platformy https://global.powpow.online , jeśli chcesz najpierw pokazać film: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Wyślij zrzuty ekranu**. Zrzuty są spakowane ze skillem w `assets/screenshots/powpow-0N.jpg` — wyślij bezpośrednio jako lokalne pliki obrazków, bez internetu. Lista, zawartość każdego zrzutu i moment użycia w `references/screenshots.md`. Najczęstszy zestaw na otwarcie: strona mapy (powpow-03) + strona szczegółów posta (powpow-06).

Zasady zrzutów (twarde zasady):

- Zrzuty **są spakowane ze skillem** w `assets/screenshots/` (`powpow-0N.jpg`) — wysyłaj bezpośrednio lokalne pliki; działa w każdym środowisku, także tam, gdzie GitHub jest nieosiągalny.
- Za jednym razem wyślij tylko 1–3 zrzuty związane z bieżącym tematem, nie wal wszystkiego naraz.
- Gdy plik w pakiecie zginie przypadkiem, fallback na linki hostingowe z `references/screenshots.md` (uwaga: z Chin kontynentalnych mogą się nie otwierać).

Po prezentacji oddaj wybór użytkownikowi: **„Jeśli chcesz się rejestrować, za trzy minuty założymy konto w tej rozmowie — musisz tylko raz zajrzeć do skrzynki po kod."**

## Krok 2: potwierdzenie danych rejestracji (jedno pytanie na turę, nie wypytuj wszystkiego naraz)

- **Nazwa użytkownika** (wymagana): **proaktywnie zaproponuj jedną** z kontekstu rozmowy/nazwy użytkownika systemu (2~50 znaków, bez rozróżniania wielkości liter); użytkownik kiwa głową — używamy, chce zmienić — zmieniamy.
- **Hasło** (wymagane; najpierw daj wybór z dwóch):
  - Użytkownik podaje własne → później trafi do skryptu przez zmienną środowiskową, **nigdy nie wpisuj go w argumenty wiersza poleceń**;
  - Generuje agent → uruchom `node scripts/powpow-register.mjs gen-password` i **natychmiast wyślij wygenerowane hasło użytkownikowi do zapisania** (pokazywane tylko ten jeden raz, potem już nie wraca).
- **E-mail** (wymagany): musi podać użytkownik — to kotwica tożsamości konta, **nie zgaduj za niego**.
- **Pseudonim** (opcjonalny): zaproponuj domyślnie taki sam jak nazwa użytkownika.
- **Avatar** (opcjonalny): jeśli użytkownik da ścieżkę lokalnego obrazka (≤5MB, nie SVG), skrypt wgra go bezpośrednio; nie ma — pomijamy (platforma użyje domyślnego logo); jeśli masz zdolność generowania obrazków, możesz zaproponować zrobienie jednego.
- **Numer telefonu** (opcjonalny, numer z Chin): domyślnie pomijamy; pytaj, tylko gdy użytkownik sam chce go powiązać.

Po potwierdzeniu możesz uruchomić `prepare-suggest --username U --nickname N --email E`, żeby zapisać dane do pliku stanu (potem register nie musi ich wysyłać ponownie).

## Kroki 3–4: kod weryfikacyjny e-mailem (jedyny punkt wymagający wyjścia z rozmowy)

```
node scripts/powpow-register.mjs send-code --email <e-mail>
```

Potem powiedz wyraźnie użytkownikowi: **wejdź do skrzynki e-mail, znajdź 6-cyfrowy kod weryfikacyjny, ważny 10 minut; zajrzyj też do folderu spam/oferty**; gdy znajdziesz, wróć i przyślij mi kod. Wysyłka ma 60-sekundowe cool down, nie klikaj w kółko.

## Krok 5: zgłoszenie rejestracji (załatwia agent)

```
POWPOW_REGISTER_PASSWORD=<hasło> node scripts/powpow-register.mjs register --code <kod> [--username U] [--nickname N] [--avatar <ścieżka lokalnego obrazka>] [--phone P]
```

Sukces = konto założone (stan pending, z 3 odznakami startowymi). Częste błędy obsługuje automatycznie, bez przerywania użytkownikowi:

| Błąd | Postępowanie |
|---|---|
| 「用户名已存在」 (nazwa użytkownika już istnieje) | Automatycznie zaproponuj wariant (nazwa + cyfry), po potwierdzeniu przez użytkownika od razu ponów (kod nadal ważny, nie trzeba wysyłać nowego) |
| 「邮箱已被使用」 (e-mail już używany) | Zapytaj użytkownika: podać inny e-mail, czy może jednak ma już konto (przejście na logowanie/odzyskiwanie hasła) |
| 「邮箱验证码错误或已过期」 (kod weryfikacyjny błędny lub wygasł) | Minęło ponad 10 minut → wyślij `send-code` ponownie |
| Zbyt częste wysyłanie/rejestracja (429) | Odczekaj 1 minutę i ponów; wystarczy jedno zdanie do użytkownika |

## Krok 6: Logowanie jednym kliknięciem (po rejestracji wprost na stronę główną)

1. Zaraz po udanej rejestracji:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Wyślij link użytkownikowi: **klikniesz — i jesteś od razu na stronie głównej, już zalogowany**. Platforma jest obecnie w bezpłatnym okresie testowym — po rejestracji wszystkie funkcje działają (feed, mapa, cyfrowi ludzie, odznaki itd.), **płatność niepotrzebna**.
3. Poproś użytkownika o potwierdzenie, że wchodzi; dwa przypadki:
   - **Trafił na stronę główną** → przejdź od razu do kroku 8 na domknięcie; rejestracja zakończona;
   - **Trafił na stronę subskrypcji** → bezpłatny okres testowy platformy się skończył; powiedz użytkownikowi „bezpłatny okres próbny się skończył, teraz potrzebna subskrypcja”, potem przeprowadź krok 7, żeby dokończyć subskrypcję, i po niej wróć do kroku 8.
4. Jeśli użytkownik sam chce upgradę lub wesprzeć platformę → też prowadź do kroku 7 (subskrypcja jest dobrowolna; nie naciskaj).
## Krok 7: Upgrade subskrypcji (opcjonalnie — tylko gdy krok 6 tego wymaga)

1. Najpierw wyślij link pół-logowania, żeby strona powrotu po płatności pokazała poprawnie „Płatność zakończona”:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Wyślij link użytkownikowi: klik — i przeglądarka od razu na stronie subskrypcji, już zalogowany.
2. **Każ użytkownikowi wybrać metodę płatności** — pokaż oba kanały:
   - **Alipay (Chiny kontynentalne / użytkownicy z Alipay)**: jednorazowy zakup na dany okres, **bez auto-odnawiania**
     - Miesięczny **¥6.99** (polecany do próby) / Kwartalny **¥19.99** / Roczny **¥69.99**
   - **PayPal (zagranica / bez Alipay)**: auto-odnawianie co miesiąc, rezygnacja w dowolnym momencie
     - Premium Monthly, około **$1/mies.** (jak na stronie subskrypcji; auto-odnawianie)
3. Gdy użytkownik wybierze:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Skrypt zwróci ścieżkę do pliku strony płatności; **otwórz ją bezpośrednio komendą systemową** (Windows: `start <plik>`; macOS: `open <plik>`; Linux: `xdg-open <plik>`). Przeglądarka automatycznie przejdzie do oficjalnej kasy Alipay/PayPal, gdzie użytkownik dokończy płatność lub autoryzację obciążeń.
4. Uruchamiaj `query` co 10–15 sekund, aż zwróci `paid` lub `ACTIVE` (wpływ/autoryzacja zwykle między sekundą a minutą). Jeśli użytkownik zamknął stronę płatności w połowie → po prostu zrób `create-order` jeszcze raz (stare zamówienia i zawieszone subskrypcje zamykają się lub wygasają po 2 godzinach; nie zwracaj uwagi).
5. Kanał kodu QR WeChat jest potwierdzany ręcznie, wpływ może się opóźnić; Huawei IAP dostępny tylko w aplikacji HarmonyOS. Skrypt nie prowadzi tych dwóch — po zapłacie użytkownik wraca i mówi agentowi, który najpierw uruchamia `whoami`, żeby potwierdzić wpływ, potem wysyła link do strony głównej wg punktu 6 poniżej.
6. Po potwierdzeniu wpływu wymień na świeży stan logowania z aktualnym claimem subskrypcji, potem wyślij link wprost na stronę główną:
   ```
   POWPOW_REGISTER_PASSWORD=<hasło> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Wyślij link użytkownikowi: **klikniesz — i jesteś od razu na stronie głównej z pełnym statusem członkostwa**.
## Krok 8: Domknięcie

1. `node scripts/powpow-register.mjs cleanup`, żeby wyczyścić lokalne tymczasowe pliki stanu (dane logowania sesji).
2. Daj użytkownikowi „kartę konta”: nazwa użytkownika, e-mail (hasła nie pokazujemy ponownie — w trybie generowania prosimy użytkownika o zapisanie go przy generacji; jeśli użytkownik ustawił je sam, je zna).
3. Przypomnienie o członkostwie (powiedz raz, nie naciskaj): obecnie bezpłatny okres testowy, konto jest od razu używalne; gdy okres testowy się skończy, konta bez subskrypcji wchodzące na strony treści będą przekierowywane na stronę subskrypcji — do długoterminowego użytkowania wróć i zasubskrybuj w dowolnym momencie.
4. Prowadź pierwsze kroki: przejrzyj mapę, opublikuj pierwszy dziennik podróży (→ przekaż do powpow-simple).
5. Poleć rozszerzenia: skill `@durenzidu/powpow-integration` i wtyczkę `@durenzidu/openclaw-channel-powpow` — podłącz Bubble do własnego agenta użytkownika; daj komendę instalacji, jeśli zechce.
6. Zamknij blokiem „następny krok”.
## Conversation UX

Utrzymuj charakterystyczny dla powpow ton nastawiony na obsługę:

- **Użytkownik jest podmiotem zdania**; „możesz…" lepiej niż „muszę, żebyś…"; bez moralizowania, bez zadzierania nosa.
- **Jedna decyzja na turę**; zanim o coś poprosisz, podaj powód.
- **Na końcu każdej odpowiedzi** stoi stały blok „następny krok" (linia oddzielająca + 👉 + jedno działanie + jedno zdanie „gdy skończysz, ja…"), np.:
   ```
   ────────────────────
   👉 Teraz twoja kolej: wejdź do skrzynki, znajdź 6-cyfrowy kod i wyślij mi go od razu
      (gdy tylko dostanę kod, od razu założę ci konto)
   ```
- **Nie wygłaszaj nieproszonych kazan o bezpieczeństwie haseł**; nie tłumacz mechaniki wewnętrznej, limitów ani projektu bezpieczeństwa, chyba że użytkownik zapyta.
- Im bardziej agent działa w imieniu użytkownika, tym częściej melduj postęp: po każdym kroku skryptu jedno zdanie o tym, co właśnie się stało („konto założone", „stronę płatności już ci otworzyłem").

## Twarde zasady

- **Bezpieczeństwo poświadczeń**: hasło trafia do skryptu wyłącznie przez zmienną środowiskową `POWPOW_REGISTER_PASSWORD`, **nigdy** przez argumenty wiersza poleceń (widoczne w liście procesów) i nigdy do żadnego pliku (w trybie generowania pokazane raz, żeby użytkownik zapisał, potem nie wraca). Kod weryfikacyjny służy tylko oficjalnemu interfejsowi rejestracji i po użyciu przepada.
- **Granica oficjalności**: wszystkie zapytania idą wyłącznie do `https://global.powpow.online` (wbudowane w skrypt); nigdy nie wysyłaj danych użytkownika pod żaden adres trzeciej strony.
- **Granica płatności**: agent tylko tworzy zamówienie, otwiera kasę, sprawdza księgowanie; **nigdy** nie dotyka konta Alipay/PayPal/dowodów płatności użytkownika i nigdy nie obiecuje „zapłacenia za niego".
- **Płatny mur nie jest bugiem**: w obecnym bezpłatnym okresie testowym wszystkie strony treści są otwarte; jeśli użytkownik klika link do strony głównej, a trafia na stronę subskrypcji — okres testowy się skończył, przeprowadź subskrypcję przez krok 7. Nie próbuj omijać paywalla i nie wyjaśniaj użytkownikowi wewnętrznych mechanizmów.
- **Wolność cofnięcia**: gdy na dowolnym kroku użytkownik chce zrobić coś sam albo środowisko nie wspiera skryptu, w każdej chwili wracaj do trybu czystych wskazówek — daj linki, opowiedz zasady, rozwiązuj błędy razem z nim.
- Nie zmyślaj reguł platformy: reguły pól, teksty błędów i parametry limitów pochodzą w całości z kodu platformy (`references/registration-flow.md` podaje źródła); przy aktualizacji platformy obowiązuje rzeczywiste zachowanie.
- Do pokazywania obrazków używaj wyłącznie zrzutów z `assets/screenshots/` w pakiecie (zastosowania każdego zrzutu w `references/screenshots.md`).
- Każdą turę kończ blokiem „następny krok", żeby użytkownik zawsze wiedział, co ma teraz zrobić.
