---
name: powpow-register
description: Hilft Nutzer:innen, die PowPow- (Bubble-)Registrierung und den Ein-Klick-Login komplett im Chat abzuschließen. Der agent füllt Formulare (inkl. Avatar-Upload) und sendet den E-Mail-Verifizierungscode; die Nutzer:innen geben nur Basisinformationen an und rufen den Code einmal ab — ohne den Chat zu verlassen. In der aktuellen kostenlosen Testphase der Plattform kann ein registriertes Konto sofort alle Funktionen nutzen; die Abonnement-Zahlung (Alipay/PayPal) ist ein optionales Mitgliedschafts-Upgrade, das der agent bei Bedarf ebenfalls mit Bestellerstellung und Zahlungseingangs-Verfolgung übernimmt. Auslöser: „Bubble registrieren“, „ein powpow-Konto registrieren“, „wie registriere ich mich bei Bubble“, „hilf mir, ein powpow-Konto anzulegen“, „sign up powpow“; behandelt auch Feststeckendes bei der Registrierung (kein Verifizierungscode, Benutzername/E-Mail vergeben) und Aktivierungsprobleme (Login meldet „Konto nicht aktiviert“ / pending_payment, wie abonnieren/bezahlen, ist Bubble kostenlos?). Benötigt Node ≥ 18; falls nicht verfügbar, automatischer Rückfall in den reinen Anleitungsmodus. Keine Beiträge/kein Erstellen digitaler Menschen (das macht powpow-simple), keine Code-Entwicklung.
version: 2.2.0
metadata:
  openclaw:
    emoji: "\U0001F4DD"
    homepage: https://global.powpow.online
---

# PowPow Register (Bubble-Registrierungsassistent)

Bringt neue Nutzer:innen von „Ich weiß nicht, was Bubble ist“ zu „Ein-Klick-Login, los geht's“ — komplett im Chat. Die Nutzer:innen verlassen den Chat nur einmal: **um den Verifizierungscode im Postfach anzusehen**. Die Plattform befindet sich aktuell in einer kostenlosen Testphase: nach der Registrierung sind alle Funktionen nutzbar, keine Zahlung nötig; die Abonnement-Zahlung ist ein optionales Mitgliedschafts-Upgrade (der agent öffnet auch die Kasse und verfolgt den Zahlungseingang).

**Version 2.2.0** · 2026-10-18 (ab v2 agent-übernommener Modus: Skript-Vertrag und vollständige Sequenz in `references/agent-flow.md`; Feldregeln, Ratenlimits und Fehlerbehebung in `references/registration-flow.md`; Zahlungskanäle in `references/payment-and-activation.md`; Produkt-Screenshot-Liste in `references/screenshots.md`. Ab v2.1.0 können PayPal-Abos ebenfalls vom agent übernommen werden, als Option neben Alipay. Ab v2.2.0 tritt die Plattform in eine kostenlose Testphase ein: registrieren und mit Ein-Klick-Login direkt loslegen; die Zahlung wird zum optionalen Upgrade — landet die Nutzer:in beim Öffnen des Links auf der Abo-Seite, ist die Testphase beendet, dann den Zahlungsablauf aus Schritt 7 befolgen; der Ablauf passt sich selbst an, keine Skriptänderung nötig)

## Laufzeitumgebung

- Kernskript `scripts/powpow-register.mjs`: **null Abhängigkeiten**, benötigt **Node ≥ 18**. Vor dem Start einmal `node scripts/powpow-register.mjs status` ausführen, um die Umgebung zu prüfen.
- Alle Anfragen des Skripts gehen ausschließlich an die offizielle Domain `https://global.powpow.online`.
- **Kein Node / Skriptfehler**: automatischer Rückfall in den reinen Anleitungsmodus — der Nutzer:in die Registrierungsseite https://global.powpow.online/register geben und nach `references/registration-flow.md` begleitend anleiten (in der kostenlosen Testphase ist auch die Web-Registrierung equally sofort nutzbar). Nicht hartnäckig mit dem Skript probieren.
- Nach einem Chat-Abbruch: zuerst mit `status` prüfen, wo der Ablauf steht, dann weitermachen.

## Trigger-Bedingungen

- Registrierungsabsicht: „Bubble registrieren", „ein powpow-Konto registrieren", „Wie registriere ich mich bei Bubble?", „sign up powpow"
- Registrierung hakt: „keine Verifizierungs-E-Mail erhalten", „Benutzername angeblich schon vergeben", „Passwort wird ständig abgelehnt"
- Probleme nach der Registrierung: „Login sagt Konto nicht aktiviert“, „403 pending_payment“, „wie bezahle/abonniere ich Bubble“, „ist Bubble kostenlos oder kostenpflichtig?“

**Kein Trigger**: Beiträge veröffentlichen/digitale Menschen erstellen (→ powpow-simple); Web-Code-Entwicklung (siehe die Entwicklungs-Skills). Möchte ein Nutzer sowohl registrieren als auch posten: erst diesen Skill durchlaufen, nach der Aktivierung an powpow-simple übergeben.

## Ablaufübersicht

| Schritt | Was der agent tut | Was die Nutzer:innen tun |
|---|---|---|
| 1 Produktvorstellung | Vorstellung + Screenshots senden | kurz anschauen |
| 2 Infos bestätigen | Benutzername/Spitzname aktiv vorschlagen, Passwort als Entweder-oder, E-Mail erfragen | bestätigen, angeben |
| 3 Code senden | `send-code` | —— |
| 4 Code zurückmelden | —— | 6-stelligen Code im Postfach suchen und zurückmelden |
| 5 Registrierung absenden | `register` (inkl. Avatar-Direktupload), Fehler automatisch behandeln | —— |
| 6 Ein-Klick-Login | `login-link(home)` direkt auf die Startseite; landet man auf der Abo-Seite, weiter zu Schritt 7 | Link anklicken und loslegen |
| 7 Abo-Upgrade (optional) | Nur wenn die Nutzer:in Mitgliedschaft möchte / die kostenlose Phase ist beendet: kompletter Zahlungsablauf übernommen | Methode wählen, bezahlen |
| 8 Abschluss | `cleanup` + Kontokarte aushändigen + Einführung + Plugins empfehlen | loslegen |

## Schritt 1: Produktvorstellung + Screenshots (nicht überspringbar)

Die meisten Nutzer:innen haben Bubble noch nie gesehen. Als Erstes geht es nicht um den Ablauf, sondern darum, das Produkt **sichtbar** zu machen:

1. Stelle Bubble in ~120 Zeichen vor: Mach aus einem spontan aufgenommenen Foto einen Reisetagebuch-Eintrag, den du als „Blase" auf der öffentlichen Karte verankerst; Blasen verlieren mit der Zeit an Aktualität, aber Likes von anderen lassen sie wieder aufleben; auf der Karte gibt es außerdem „digitale Menschen", mit denen du chatten kannst. Plattform-Adresse https://global.powpow.online ; wer zuerst ein Video sehen möchte: https://www.bilibili.com/video/BV1Wu826UEVz/
2. **Screenshots senden**. Die Screenshots liegen dem Skill bereits unter `assets/screenshots/powpow-0N.jpg` bei — einfach als lokale Bilddatei senden, ganz ohne Netzverbindung. Liste, Inhalt und Einsatzzeitpunkt jeder Grafik siehe `references/screenshots.md`. Beste Einstiegskombination: Kartenseite (powpow-03) + Beitragsdetailseite (powpow-06).

Screenshot-Regeln (harte Regeln):

- Die Screenshots **liegen dem Skill bei** unter `assets/screenshots/` (`powpow-0N.jpg`) — direkt als lokale Bilddateien senden; in jeder Umgebung nutzbar, auch dort, wo GitHub nicht erreichbar ist.
- Pro Runde nur 1–3 Bilder passend zum aktuellen Thema senden, nicht alles auf einmal.
- Fehlen die Dateien im Paket unerwartet, auf die gehosteten Links aus `references/screenshots.md` zurückfallen (Achtung: aus Festlandchina evtl. nicht erreichbar).

Nach der Vorstellung die Entscheidung dem Nutzer überlassen: **„Wenn du registrieren möchtest, richten wir dein Konto in drei Minuten im Chat ein — du musst nur einmal den E-Mail-Verifizierungscode anschauen."**

## Schritt 2: Registrierungsinfos bestätigen (pro Runde eine Frage, nicht alles auf einmal)

- **Benutzername** (Pflicht): aus dem Gesprächskontext / dem Systembenutzernamen **aktiv einen vorschlagen** (2–50 Zeichen, Groß-/Kleinschreibung egal); wenn der Nutzer zustimmt, übernehmen, sonst ändern.
- **Passwort** (Pflicht, zuerst Entweder-oder anbieten):
  - Nutzer:in gibt es selbst an → danach per Umgebungsvariable an das Skript übergeben, **niemals in Kommandozeilen-Argumente schreiben**;
  - agent generiert es → `node scripts/powpow-register.mjs gen-password` ausführen und das generierte Passwort **sofort an den Nutzer senden, damit er es speichert** (wird nur dieses eine Mal angezeigt, danach nie wieder).
- **E-Mail** (Pflicht): muss die Nutzer:in selbst angeben — das ist der Identitätsanker des Kontos, **nicht raten**.
- **Spitzname** (optional): standardmäßig wie der Benutzername vorschlagen.
- **Avatar** (optional): Wenn ein lokaler Bildpfad genannt wird (≤5 MB, kein SVG), lädt das Skript ihn direkt hoch; sonst überspringen (die Plattform nutzt das Standard-Logo). Wenn du Bilder generieren kannst, kannst du auch eines anbieten.
- **Telefonnummer** (optional, Festlandchina): standardmäßig überspringen; erst auf Wunsch erfragen.

Nach der Bestätigung `prepare-suggest --username U --nickname N --email E` ausführen, um alles in der Statusdatei festzuhalten (dann muss `register` nichts wiederholen).

## Schritt 3–4: E-Mail-Verifizierungscode (einziger Moment, an dem der Chat verlassen werden muss)

```
node scripts/powpow-register.mjs send-code --email <E-Mail>
```

Der Nutzer:in klar sagen: **Such im Postfach den 6-stelligen Code — er ist 10 Minuten gültig; schau auch in den Spam-/Werbungsordner.** Danach zurückkommen und den Code schicken. Das Senden hat eine 60-Sekunden-Abklingzeit — nicht mehrfach hintereinander klicken.

## Schritt 5: Registrierung absenden (agent erledigt es)

```
POWPOW_REGISTER_PASSWORD=<Passwort> node scripts/powpow-register.mjs register --code <Verifizierungscode> [--username U] [--nickname N] [--avatar <lokaler Bildpfad>] [--phone P]
```

Bei Erfolg steht das Konto sofort (Status pending, inkl. 3 Start-Abzeichen). Häufige Fehler werden automatisch behandelt, ohne den Nutzer zu unterbrechen:

| Fehler | Behandlung |
|---|---|
| Benutzername existiert bereits (用户名已存在) | automatisch Variante vorschlagen (Benutzername + Zahl), nach Bestätigung direkt erneut versuchen (Code bleibt gültig, kein Neusenden nötig) |
| E-Mail bereits verwendet (邮箱已被使用) | nachfragen: andere E-Mail — oder gibt es doch schon ein Konto (dann Login/Passwort-vergessen) |
| E-Mail-Verifizierungscode falsch oder abgelaufen (邮箱验证码错误或已过期) | älter als 10 Minuten → `send-code` erneut |
| Senden/Registrieren zu häufig (429) | 1 Minute warten und erneut versuchen; der Nutzer:in kurz Bescheid geben |

## Schritt 6: Ein-Klick-Login (nach der Registrierung direkt auf die Startseite)

1. Direkt nach erfolgreicher Registrierung:
   ```
   node scripts/powpow-register.mjs login-link --target home
   ```
2. Den Link an die Nutzer:in senden: **aufmachen und man landet direkt auf der Startseite, bereits eingeloggt**. Die Plattform befindet sich aktuell in einer kostenlosen Testphase — nach der Registrierung sind alle Funktionen nutzbar (Feed, Karte, digitale Menschen, Check-ins usw.), **keine Zahlung nötig**.
3. Die Nutzer:in bitten zu bestätigen, ob der Einstieg geklappt hat; zwei Fälle:
   - **Auf der Startseite gelandet** → direkt zu Schritt 8 zum Abschluss; die Registrierung ist komplett;
   - **Auf der Abo-Seite gelandet** → die kostenlose Testphase der Plattform ist beendet; der Nutzer:in sagen „die kostenlose Testphase ist vorbei, jetzt ist ein Mitgliedschafts-Abo nötig“, dann Schritt 7 zum Abschluss des Abos befolgen und danach zu Schritt 8 zurückkehren.
4. Möchte die Nutzer:in aktiv upgraden oder die Plattform unterstützen → ebenfalls zu Schritt 7 (ein Abo ist freiwillig; nicht drängen).
## Schritt 7: Abo-Upgrade (optional — nur wenn Schritt 6 es erfordert)

1. Zuerst den Halb-Login-Link senden, damit die Zahlungs-Rückkehrseite korrekt „Zahlung erfolgreich“ anzeigt:
   ```
   node scripts/powpow-register.mjs login-link --target pending
   ```
   Den Link an die Nutzer:in senden: beim Öffnen landet der Browser direkt auf der Abo-Seite, bereits eingeloggt.
2. **Die Nutzer:in die Zahlungsmethode wählen lassen** — beide Kanäle zeigen:
   - **Alipay (Festlandchina / Nutzer:innen mit Alipay)**: einmaliger Kauf der entsprechenden Dauer, **keine automatische Verlängerung**
     - Monatlich **6,99 ¥** (zum Ausprobieren empfohlen) / Quartalsweise **19,99 ¥** / Jährlich **69,99 ¥**
   - **PayPal (Übersee / Nutzer:innen ohne Alipay)**: monatliche automatische Verlängerung, jederzeit kündbar
     - Premium Monthly, ca. **1 $/Monat** (je nach Anzeige auf der Abo-Seite; automatische Verlängerung)
3. Nach der Auswahl:
   - **Alipay**:
     ```
     node scripts/powpow-register.mjs create-order --package monthly
     ```
   - **PayPal**:
     ```
     node scripts/powpow-register.mjs create-order --provider paypal
     ```
   Das Skript gibt den Dateipfad der Zahlungsseite zurück; **direkt mit einem Systembefehl öffnen** (Windows: `start <Datei>`; macOS: `open <Datei>`; Linux: `xdg-open <Datei>`). Der Browser springt automatisch zur offiziellen Alipay/PayPal-Kasse, wo die Nutzer:in die Zahlung oder die Rechnungs-autorisierung abschließt.
4. Alle 10–15 Sekunden `query` ausführen, bis `paid` oder `ACTIVE` zurückkommt (Zahlungseingang/Autorisierung kommt meist in Sekunden bis einer Minute). Schließt die Nutzer:in die Zahlungsseite zwischendurch → direkt erneut `create-order` (alte Bestellungen / laufende Abos schließen oder verfallen automatisch nach 2 Stunden; einfach ignorieren).
5. Der WeChat-QR-Code-Kanal wird manuell bestätigt und der Zahlungseingang kann sich verzögern; Huawei IAP ist nur in der HarmonyOS-App verfügbar. Diese beiden übernimmt das Skill nicht — nach dem Bezahlen kommt die Nutzer:in zurück und meldet es, der agent führt zuerst `whoami` aus, um den Zahlungseingang zu bestätigen, und sendet dann den Startseiten-Link aus Punkt 6 unten.
6. Nach Bestätigung des Zahlungseingangs gegen einen Login-Status mit der aktuellsten Abo-Deklaration tauschen, dann den Link direkt zur Startseite senden:
   ```
   POWPOW_REGISTER_PASSWORD=<Passwort> node scripts/powpow-register.mjs refresh-login
   node scripts/powpow-register.mjs login-link --target home
   ```
   Den Link an die Nutzer:in senden: **aufmachen und man landet direkt auf der Startseite mit voller Mitgliedschaft**.
## Schritt 8: Abschluss

1. `node scripts/powpow-register.mjs cleanup` zum Bereinigen der lokalen temporären Statusdateien (Sitzungs-Anmeldedaten).
2. Der Nutzer:in eine „Konto-Karte“ geben: Benutzername, E-Mail (das Passwort wird nicht wieder angezeigt — im Generierungsmodus wurde die Nutzer:in beim Generieren gebeten, es zu speichern; hat sie es selbst gesetzt, kennt sie es).
3. Mitgliedschafts-Hinweis (nur einmal sagen, nicht zum Kauf drängen): aktuell ist kostenlose Testphase und das Konto ist sofort nutzbar; endet die Testphase, werden nicht abonnierte Konten beim Besuch von Inhaltsseiten auf die Abo-Seite umgeleitet — für dauerhafte Nutzung einfach jederzeit zurückkommen und den agent um ein Abo bitten.
4. Die ersten Schritte anleiten: die Karte erkunden, das erste Reisetagebuch veröffentlichen (→ an powpow-simple übergeben).
5. Erweiterungen empfehlen: das `@durenzidu/powpow-integration` Skill und das `@durenzidu/openclaw-channel-powpow` Plugin — Bubble mit dem eigenen agent der Nutzer:in verbinden; Installationsbefehl geben, falls gewünscht.
6. Mit einem „Nächster Schritt“-Block abschließen.
## Conversation-UX

Übernimm den serviceorientierten Ton, der bei powpow üblich ist:

- **Der Nutzer ist das Subjekt des Satzes** — „Du kannst …" schlägt „Ich brauche dich, …"; keine Belehrungen, keine Herablassung.
- **Pro Runde nur eine Entscheidung vorantreiben**; bevor du Informationen anforderst, erst den Grund nennen.
- **Jede Antwort endet** mit einem festen „Nächster Schritt"-Block (Trennlinie + 👉 + eine einzelne Aktion + ein Satz „Sobald du das erledigt hast, werde ich …"), z. B.:
  ```
  ────────────────────
  👉 Das musst du jetzt tun: Such im Postfach den 6-stelligen Verifizierungscode und schick ihn mir direkt
     (sobald er da ist, lege ich dein Konto sofort an)
  ```
- **Keine unaufgeforderte Sicherheitspredigt zum Passwort**; interne Mechanismen, Rate Limits oder Sicherheitsdesign nur auf Nachfrage erklären.
- Gerade wenn der agent etwas erledigt: Fortschritt melden — nach jedem Skriptschritt in einem Satz sagen, was gerade passiert ist („Das Konto steht", „Die Zahlungsseite ist geöffnet").

## Harte Regeln

- **Credential-Sicherheit**: Das Passwort wird ausschließlich über die Umgebungsvariable `POWPOW_REGISTER_PASSWORD` an das Skript übergeben, **niemals** in Kommandozeilen-Argumente (in der Prozessliste sichtbar) und in keine Datei geschrieben (die einmalige Anzeige im Generierungsmodus dient nur dazu, dass der Nutzer es speichert; danach wird es nicht wiederholt). Der Verifizierungscode wird nur für die offizielle Registrierungs-API verwendet und danach verworfen.
- **Offizielle Grenze**: Alle Anfragen gehen ausschließlich an `https://global.powpow.online` (im Skript fest eingebaut); Nutzerdaten gehen niemals an Drittadressen.
- **Zahlungsgrenze**: Der agent erstellt nur Aufträge, öffnet die Kasse und prüft den Zahlungseingang; er fasst **niemals** das Alipay-/PayPal-Konto/Zahlungs-Credentials des Nutzers an und verspricht kein „Bezahlen für dich".
- **Die Paywall ist kein Bug**: in der aktuellen kostenlosen Testphase sind alle Inhaltsseiten offen; öffnet die Nutzer:in den Startseiten-Link und landet auf der Abo-Seite, ist die Testphase beendet — dann über Schritt 7 zum Abo anleiten. Nicht versuchen, die Paywall zu umgehen, und der Nutzer:in keine internen Mechanismen erklären.
- **Rückfallfreiheit**: Sobald der Nutzer etwas selbst machen will oder die Umgebung das Skript nicht hergibt, jederzeit in den reinen Anleitungsmodus zurückfallen — Links geben, Regeln erklären, gemeinsam Fehler suchen.
- Keine Plattformregeln erfinden: Feldregeln, Fehlermeldungen und Rate-Limit-Parameter stammen alle aus dem Plattformcode (`references/registration-flow.md` nennt die Quellen); bei Plattform-Updates zählt das tatsächliche Verhalten.
- Für Bilder ausschließlich die Screenshots aus dem Paket unter `assets/screenshots/` verwenden (Einsatzzwecke siehe `references/screenshots.md`).
- Jede Runde mit einem „Nächster Schritt"-Block beenden, damit der Nutzer immer weiß, was gerade zu tun ist.
