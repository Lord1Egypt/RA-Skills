# Zrzuty ekranu interfejsu produktu — powpow-register

Do użytku doraźnego w czasie pracy. Gdy użytkownik nie ma pojęcia o Bańce albo potrzebuje „zobaczyć", jak
produkt wygląda, wyślij po prostu odpowiedni zrzut.

## Położenie obrazków

- Sześć zrzutów **jest spakowanych ze skillem**, leży w `assets/screenshots/powpow-0N.jpg` (`N` to 1–6).
  Wysyłaj bezpośrednio jako lokalne pliki obrazków — bez internetu, działa w każdym środowisku (także tam,
  gdzie GitHub jest nieosiągalny).
- Fallback tylko przy przypadkowej utracie plików z pakietu: hostowana kopia
  `https://raw.githubusercontent.com/durenzidu/durenzidu/main/screenshots/powpow-0N.jpg` albo mirror
  `https://cdn.jsdelivr.net/gh/durenzidu/durenzidu@main/screenshots/powpow-0N.jpg`
  (uwaga: oba mogą się nie otwierać z Chin kontynentalnych — przedkładaj pliki z pakietu).
- Za jednym razem wysyłaj tylko 1–3 obrazki związane z bieżącym tematem.

## Lista

### powpow-01.jpg — strona szczegółów człowieka cyfrowego

![strona szczegółów człowieka cyfrowego](../assets/screenshots/powpow-01.jpg)

Karta osoby rzeczywistej/postaci historycznej przeprowadzonej w cyfrowego człowieka: status online,
lokalizacja, zarys sylwetki, „zacznij rozmowę" itd.
**Użycie**: przy przedstawianiu „po rejestracji możesz rozmawiać z cyfrowymi ludźmi na mapie".

### powpow-02.jpg — strona edycji posta

![strona edycji posta](../assets/screenshots/powpow-02.jpg)

Interfejs edycji do pisania postów/dzienników z podróży, z grupą pływających przycisków w prawym dolnym rogu.
**Użycie**: gdy użytkownik pyta „co będę mógł robić po rejestracji", „gdzie się pisze".

### powpow-03.jpg — strona mapy (Bańka + cyfrowi ludzie)

![strona mapy](../assets/screenshots/powpow-03.jpg)

Pełny widok mapy publicznej: posty z lokalizacją zbierają się na mapie jako „bańki", a cyfrowi ludzie są
przypięci awatarem w realnych miejscach.
**Użycie**: **główny zrzut na otwarcie prezentacji produktu** — „twój dziennik z podróży stanie się bańką na
mapie".

### powpow-04.jpg — profil użytkownika (aktywa cyfrowe)

![profil użytkownika](../assets/screenshots/powpow-04.jpg)

Własna strona użytkownika: znajomi/obserwowani/obserwujący oraz „aktywa cyfrowe" — saldo odznak, moje bańki,
moi cyfrowi ludzie.
**Użycie**: pokazywanie, gdzie siedzą odznaki, gdy mówisz „za rejestrację dostajesz gratis 3 odznaki"; gdy
użytkownik pyta „jakie mam aktywa".

### powpow-05.jpg — strona postępu fabuły

![strona postępu fabuły](../assets/screenshots/powpow-05.jpg)

Fabularna rozgrywka wewnątrz platformy (przykład „Yongle·1421"): postęp rozdziałów, zdobywanie odznak,
odgrywanie ról.
**Użycie**: gdy użytkownik pyta „co oprócz postowania", „jak zdobywać odznaki".

### powpow-06.jpg — strona szczegółów posta (gotowy przykład)

![strona szczegółów posta](../assets/screenshots/powpow-06.jpg)

Opublikowany dziennik z podróży: autor, tag lokalizacji, treść, zdjęcia; na dole lubienie/komentowanie/
udostępnianie/zapisanie.
**Użycie**: **drugi zrzut na otwarcie** — „to właśnie widzą inni, klikając twoją bańkę na mapie".

## Ściąga: scenariusz po scenariuszu

| Co mówi użytkownik / bieżący etap | Który zrzut wysłać |
|---|---|
| Otwarcie, przedstawianie „czym jest Bańka" | powpow-03 + powpow-06 |
| „Co będę mógł robić po rejestracji?" | powpow-02 + powpow-01 |
| „Co to odznaki / co mam?" | powpow-04 |
| „Co oprócz postowania?" | powpow-05 |
| Rozwiązywanie błędów rejestracji/subskrypcji | Zwykle obrazki niepotrzebne; wyślij tylko wtedy, gdy faktycznie trzeba pokazać położenie strony |

## Uwagi serwisowe

- Obrazki w `assets/screenshots/` to główna kopia dystrybuowana z pakietem. Gdy zrzuty trzeba odświeżyć,
  podmień plik o tej samej nazwie w `assets/screenshots/` (zachowuj nazewnictwo `powpow-0N.jpg`) i wydaj nową
  wersję.
- Hostowaną kopię w publicznym repo `durenzidu/durenzidu` (katalog `screenshots/`) trzymaj jako zapasowy
  mirror, aktualizowany równolegle z plikami w pakiecie.
- Obecna galeria **nie ma** zrzutów strony rejestracji i strony subskrypcji. Jeśli kiedyś je dodacie (np.
  `powpow-07.jpg` strona rejestracji, `powpow-08.jpg` strona subskrypcji), wrzuć pliki do
  `assets/screenshots/` i dopisz sekcję w tym samym formacie; tekst prezentacji w SKILL.md może się przy
  okazji do nich odwołać.
