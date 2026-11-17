# Proces załatwiania przez agenta i kontrakt skryptu — powpow-register

Szczegóły wykonania każdego kroku ze SKILL.md. Wszystkie polecenia mają postać `node scripts/powpow-register.mjs
<podpolecenie> [argumenty]`; skrypt ma **zero zależności**, wymaga **Node ≥ 18**, a wszystkie zapytania idą
wyłącznie do `https://global.powpow.online`.

## Projekt bezpieczeństwa (dlaczego tak)

| Rozwiązanie | Powód |
|---|---|
| Hasło wchodzi tylko przez zmienną środowiskową `POWPOW_REGISTER_PASSWORD` | Argumenty wiersza poleceń procesu są widoczne dla innych procesów na tej samej maszynie (powierzchnia wycieku argv); zmienną środowiskową skrypt czyta i od razu używa |
| Hasło **nigdy nie trafia do pliku stanu**, nigdy nie pojawia się w logach | Plik stanu może zostać na dysku; w trybie generowania w rozmowie pokazywany jest raz, żeby użytkownik zapisał |
| Plik stanu w systemowym katalogu tymczasowym (`os.tmpdir()/powpow-register-state.json`, 0600) | Zawiera tylko pięć pól email / username / nickname / token / outTradeNo; `cleanup` czyści jednym ruchem |
| JWT zdobyty przez agenta jest wymieniany na cookie przeglądarki przez oficjalny endpoint `me?token=` | Oficjalny mostek platformy zaprojektowany pod WebView HarmonyOS; weryfikacja podpisu sprawdza tylko podpis + termin ważności, nie wiąże odcisku urządzenia, więc przeglądarka użytkownika może go użyć |
| Płatność to tylko create-order / query / otwarcie kasy | Akt płatności i dowody płatności na zawsze zostają między użytkownikiem a oficjalną kasą Alipay, agent ich nie dotyka |

## Spis poleceń

| Polecenie | Kluczowe argumenty | Działanie / moment |
|---|---|---|
| `status` | —— | Podgląd postępu procesu (czyta plik stanu); po przerwaniu rozmowy uruchom najpierw to |
| `gen-password` | —— | Generuje mocne hasło 24-znakowe (wielkie + małe litery + cyfry); stdout pokazuje je **tylko ten jeden raz** |
| `prepare-suggest` | `--username --nickname --email` | Zapisuje potwierdzone dane do pliku stanu (potem register nie musi ich wysyłać ponownie) |
| `send-code` | `--email` | Wyzwala wysyłkę 6-cyfrowego kodu weryfikacyjnego (ważny 10 minut, cool down 60 s) |
| `register` | `--code` (wymagane); `--username --nickname --avatar --phone` (opcjonalne; jeśli są w pliku stanu, nie trzeba podawać) | Zakłada konto pending; hasło przez zmienną środowiskową `POWPOW_REGISTER_PASSWORD`; po sukcesie JWT automatycznie ląduje w pliku stanu |
| `login-link` | `--target pending` lub `--target home` | Generuje link logowania jednym kliknięciem (schemat dwóch linków, patrz poniżej) |
| `create-order` | `--package monthly\|quarterly\|yearly` (domyślnie Alipay)<br>`--provider alipay\|paypal` | Tworzy zamówienie płatności; Alipay zwraca ścieżkę pliku strony płatności + outTradeNo, PayPal zwraca ścieżkę pliku strony autoryzacji + subscriptionId (automatycznie wpisywane do pliku stanu) |
| `query` | —— | Sprawdza status zamówienia/subskrypcji. Alipay: `paid / pending / closed / unknown`; PayPal: `ACTIVE / PENDING`; odpytywanie co 10–15 s |
| `refresh-login` | hasło przez zmienną środowiskową | Ponowne logowanie na **nowy JWT** (claim subskrypcji przechodzi z NONE na ACTIVE); po zaksięgowaniu płatności obowiązkowo uruchomić |
| `whoami` | —— | Tokenem z pliku stanu sprawdza konto i status subskrypcji (weryfikacja, czy aktywacja zaskoczyła) |
| `cleanup` | —— | Usuwa plik stanu (obowiązkowo na zamknięciu) |

**Przekazywanie zmiennej środowiskowej** (hasło nigdy nie wchodzi na wiersz poleceń):

```bash
# bash / zsh / WSL
POWPOW_REGISTER_PASSWORD='<hasło>' node scripts/powpow-register.mjs register --code 123456
# PowerShell
$env:POWPOW_REGISTER_PASSWORD = '<hasło>'; node scripts/powpow-register.mjs register --code 123456
# cmd
set POWPOW_REGISTER_PASSWORD=<hasło> && node scripts/powpow-register.mjs register --code 123456
```

## Mechanizm dwóch linków (kluczowa konstrukcja)

Stan logowania platformy to ciasteczko HttpOnly, którego agent nie może posadzić w przeglądarce bezpośrednio; mostem jest oficjalny punkt
`/api/auth/me?token=<JWT>&redirect=<ścieżka w serwisie>`: weryfikacja podpisu → automatyczne utworzenie
sesji → `Set-Cookie: powpow_token` (HttpOnly / SameSite=Lax / 7 dni) → walidacja
redirect (musi zaczynać się pojedynczym ukośnikiem, `//` i backslashy zabronione, po sparsowaniu musi być same-origin) → 307 tymczasowe przekierowanie na stronę docelową.

Są dwa cele linków, **najpierw generuj home, a czy przechodzić przez pending — decyduj po tym, gdzie użytkownik wylądował**:

- **link home (domyślnie, `--target home` → ląduje na `/`)**: generowany i wysyłany użytkownikowi od razu po udanej rejestracji.
  W bezpłatnym okresie testowym użytkownik trafia wprost na stronę główną, wszystko działa; **jeśli kliknie link, a trafi na stronę subskrypcji — bezpłatny okres testowy się skończył** — przełącz się na przepływ płatności (patrz niżej); bez zmiany skryptu i bez ponownej rejestracji.
- **link pending (w przepływie płatności, `--target pending` → ląduje na `/subscription`)**:
  przeglądarka użytkownika wchodzi w stan „pół-logowania”: strona subskrypcji i strona powrotu po płatności są widoczne i umożliwiają działanie. Po wpływie płatności
  uruchom `refresh-login`, żeby wymienić na nowy JWT z claimem ACTIVE, potem wyślij link home jeszcze raz dla pełnego statusu członkostwa.

## Pełna sekwencja

### Ścieżka szybka (w bezpłatnym okresie testowym — zdecydowana większość przypadków)

```
1.  status                          # samosprawdzenie środowiska
2.  (krok 2: rozmowa potwierdzająca dane, hasło do wyboru; tryb generowania: gen-password → poproś od razu użytkownika o zapisanie)
3.  prepare-suggest --username U --nickname N --email E
4.  send-code --email E             # → użytkownik sprawdza kod w skrzynce (jedyny wyjście z rozmowy)
5.  POWPOW_REGISTER_PASSWORD=*** register --code 123456 [--avatar pic.jpg]
6.  login-link --target home        # → wyślij link użytkownikowi; jedno kliknięcie i jest na stronie głównej
7.  (użytkownik potwierdza, że wszedł) → od razu domknięcie: cleanup + karta konta + prowadzenie pierwszych kroków
```

### Ścieżka płatności (gdy użytkownik chce członkostwa lub bezpłatny okres się skończył)

```
1–5. Jak w ścieżce szybkiej (stan ma już token po udanym register)
6.  login-link --target pending     # → link pół-logowania, strona powrotu po płatności działa
7.  (użytkownik wybiera metodę płatności)
    # Alipay: create-order --package monthly|quarterly|yearly
    # PayPal: create-order --provider paypal
8.  start <plik strony płatności>   # Windows; macOS używa open, Linux xdg-open
    # → użytkownik kończy płatność/autoryzację w kasie Alipay/PayPal (opuszcza rozmowę)
9.  query (co 10–15 s) do paid / ACTIVE
10. refresh-login                   # wymiana na nowy JWT z claimem ACTIVE
11. login-link --target home        # → wyślij użytkownikowi link z pełnym członkostwem
12. whoami                          # potwierdź subscriptionStatus: ACTIVE (opcjonalnie)
13. cleanup                         # wyczyść plik stanu
```
## Mapowanie: polecenie → API platformy

| Polecenie skryptu | Interfejs platformy |
|---|---|
| `send-code` | `POST /api/auth/register/send-code` |
| `register` | `POST /api/auth/register` (multipart, bezpośrednie wgranie avatara) |
| `login-link` | `GET /api/auth/me?token=…&redirect=…` (sam link; zadziała po kliknięciu w przeglądarce) |
| `create-order` | `POST /api/payment/alipay/create-order` (Bearer, Alipay)<br>`GET /api/subscription/plans` + `POST /api/subscription/create` (Bearer, PayPal) |
| `query` | `GET /api/payment/alipay/query?outTradeNo=…` (Bearer, Alipay)<br>`GET /api/subscription/create` (Bearer, PayPal) |
| `refresh-login` | `POST /api/auth/login` (`{step:1, username, password}`) |
| `whoami` | `GET /api/auth/me?token=…` |

Źródła reguł: pola rejestracji i limity w `registration-flow.md`; pakiety i łańcuch aktywacji w
`payment-and-activation.md` (oba podają pliki kodu platformy).

## Obsługa błędów na poziomie skryptu

| Objaw | Postępowanie |
|---|---|
| `Node 版本过低` (wersja Node zbyt niska) | Powrót do trybu czystych wskazówek, nie forsuj |
| Błąd sieci / timeout | Jedna ponowna próba; przy dalszej porażce niech użytkownik sprawdzi sieć i idziemy dalej (plik stanu istnieje — od początku uruchom `status`, żeby odzyskać) |
| register zwraca błąd biznesowy (nazwa użytkownika zajęta itd.) | Obsłuż wg tabeli z kroku 5 SKILL.md, **kodu weryfikacyjnego nie trzeba wysyłać ponownie** (wciąż ważny 10 minut) |
| register zwraca 「邮箱验证码错误或已过期」 (kod weryfikacyjny błędny lub wygasł) | Minął termin → `send-code` ponownie |
| Po `create-order` użytkownik zamknął stronę płatności | Po prostu ponów `create-order` (stare zamówienie zamknie się samo po 2 h; subskrypcje PayPal w statusie PENDING wygasają po 1 h) |
| `create-order --provider paypal` zwraca 409 | Istnieje już niedokończona subskrypcja PayPal; odczekaj 1 h, aż wygaśnie, albo dokończ starą autoryzację w przeglądarce |
| `query` wciąż pending / PENDING | Użytkownik mógł nie zapłacić; zapytaj jednym zdaniem. Jeśli zapłacił → idź wg tabeli w payment-and-activation.md |
| Użytkownik klika link home, ale trafia na stronę subskrypcji | Bezpłatny okres testowy się skończył → przełącz się na przepływ płatności: `login-link --target pending` → wybór metody płatności → `create-order` |
| `refresh-login` 403 `pending_payment` | Bezpłatny okres testowy się skończył, a płatność nie wpłynęła; wróć do kroku 9 i dalej odpytuj, albo potwierdź, czy użytkownik dokończył płatność |
| Zgubiony plik stanu (przypadkiem usunięty / inna maszyna) | `whoami`/`refresh-login` nie zadziałają; niech użytkownik w przeglądarce, w której otwierał link 1, odświeży stronę subskrypcji, żeby potwierdzić stan, albo zaloguje się ponownie (tryb webowy) |

## Tryb awaryjny (czyste wskazówki)

Przy dowolnym z poniższych natychmiast wracaj do czystych wskazówek w stylu v1 i przestań męczyć skrypt:

- Brak Node ≥ 18 albo dwie porażki skryptu tego samego typu z rzędu;
- Użytkownik wprost mówi „zrobię to sam w przeglądarce";
- Polityka firmy/urządzenia blokuje skryptowi dostęp do sieci.

Po powrocie: podaj stronę rejestracji https://global.powpow.online/register (w bezpłatnym okresie testowym rejestracja przez stronę jest równie natychmiastowa; gdy potrzebna subskrypcja, podaj też stronę subskrypcji https://global.powpow.online/subscription ), diagnozuj w towarzystwie wg reguł w `registration-flow.md`, trzymaj ten sam ton i nadal kończ każdą turę blokiem „następny krok”.
https://global.powpow.online/subscription , prowadź rozwiązywanie błędów wg reguł `registration-flow.md`,
ton bez zmian, każda tura nadal kończy się blokiem „następny krok".
