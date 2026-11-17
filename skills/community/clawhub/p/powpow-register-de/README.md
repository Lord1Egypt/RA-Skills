# powpow-register

PowPow-Bubble-Registrierungsassistent (OpenClaw-Version): führt neue Nutzer:innen von „Ich weiß nicht, was Bubble ist" bis zu „Konto aktiviert, Ein-Klick-Login, loslegen" — Produktvorstellung (mit UI-Screenshots), Registrierung durch den agent (inkl. Avatar-Upload), Alipay-/PayPal-Abo-Bestellung mit Eingangsverfolgung, doppeltes Ein-Klick-Login, Fehlerbehebung.

**Ab v2.0.0 agent-übernommener Modus, ab v2.2.0 Anpassung an die kostenlose Testphase der Plattform**: das Kern-Skript `scripts/powpow-register.mjs` ist null-Abhängigkeit
(Node ≥ 18); die Nutzer:innen verlassen den Chat nur einmal: um den Verifizierungscode im Postfach anzusehen. In der aktuellen kostenlosen Testphase kann ein registriertes Konto alle Funktionen sofort nutzen — die Abo-Zahlung ist ein optionales Upgrade; endet die Testphase und die Nutzer:in landet auf der Abo-Seite, wechselt der Ablauf automatisch auf den Zahlungsweg. Ohne Node, oder wenn die Nutzer:in es selbst machen möchte, automatischer Rückfall in den reinen Anleitungsmodus.

## Installation

```
openclaw skills install @durenzidu/powpow-register
```

## Funktionen

1. **Produktvorstellung**: ~120-Zeichen-Auftakt + beiliegende UI-Screenshots (`assets/screenshots/`, 6 Stück: Kartenseite, Beitragsdetailseite usw.; je nach Szene 1–3 davon senden; kein externes Bild-Hosting nötig, offline nutzbar).
2. **Registrierung durch den agent**: aktive Vorschläge für Benutzername/Spitzname, Passwort als Entweder-oder (selbst angeben oder generieren lassen), Senden und Einreichen des Verifizierungscodes, Avatar-Direktupload (≤5 MB, kein SVG), automatische Behandlung häufiger Fehler (vergeben/abgelaufen/Rate Limit).
3. **Ein-Klick-Login (zwei Links)**: direkt nach erfolgreicher Registrierung bringt ein Login-Link die Nutzer:in direkt auf die Startseite (in der kostenlosen Testphase: aufmachen und sofort nutzbar);
   landet sie auf der Abo-Seite (Testphase beendet) oder möchte sie upgraden, den Abo-Ablauf befolgen — nach Zahlungseingang gegen einen neuen Login-Status tauschen und der Voll-Mitgliedschafts-Link bringt sie auf die Startseite
   (über die offizielle `me?token=`-Brücke der Plattform, die das HttpOnly-Cookie automatisch setzt).
4. **Abo-Zahlung**: Sowohl Alipay (Monat ¥6.99 / Quartal ¥19.99 / Jahr ¥69.99, Einmalkauf ohne automatische Verlängerung) als auch PayPal (Premium Monthly, ca. $1/Monat, automatische Verlängerung, jederzeit kündbar) bestellt der agent und pollt den Eingang; WeChat-QR/Huawei IAP nur den Weg weisen.
5. **Fehlerbehebung**: kein Verifizierungscode, Benutzername/E-Mail vergeben, 403 nicht aktiviert, Kontosperre usw. — alles aus dem Plattform-Quellcode, mit Quellenangaben.

## Dateistruktur

```
powpow-register/
├── SKILL.md                            # Hauptleitfaden (Trigger, 8-Schritte-Ablauf, Ton, harte Regeln)
├── README.md
├── .clawhubignore
├── assets/
│   └── screenshots/                    # beiliegende Produkt-Screenshots (powpow-01~06.jpg)
├── scripts/
│   └── powpow-register.mjs             # Kernskript (null Abhängigkeiten, Node≥18, 11 Unterkommandos)
└── references/
    ├── agent-flow.md                   # Skript-Vertrag, volle Sequenz, Doppellink-Mechanik, Sicherheitsdesign
    ├── registration-flow.md            # Feldregeln, Rate Limits, Fehlertabelle (mit Quellen)
    ├── payment-and-activation.md       # Alipay-vibepay-Vertrag, Aktivierungskette, Kanal-Fehlerbehebung
    └── screenshots.md                  # Screenshot-Liste + Szenen-Schnellzugriff
```

## Sicherheit

- **Passwort** wird nur per Umgebungsvariable in den Skript-Prozess übergeben — nie in Kommandozeilen-Argumente, nie auf die Platte, nie in die Statusdatei; das generierte Passwort wird genau einmal angezeigt, damit es gespeichert werden kann.
- **Verifizierungscode** wird nur für die offizielle Registrierungs-API verwendet und danach verworfen; die Statusdatei (E-Mail/Benutzername/Token/Bestellnummer) liegt im temporären Systemverzeichnis und wird am Ende per `cleanup` entfernt.
- **Zahlung**: Der agent erstellt nur Aufträge, öffnet die Kasse und prüft den Eingang; er fasst nie das Alipay-/PayPal-Konto oder Zahlungs-Credentials an und zahlt nie stellvertretend. Die Zahlung geschieht immer zwischen der Nutzerin/dem Nutzer und der offiziellen Kasse.
- Alle Anfragen gehen nur an die offizielle Domain `https://global.powpow.online`; keinerlei Schlüssel enthalten.

## Lizenz

MIT-0 (ClawHub-Einheitslizenz).

## Links

- Offizielle Website: https://global.powpow.online
- Registrierung: https://global.powpow.online/register
- Bubble entdecken (Video): https://www.bilibili.com/video/BV1Wu826UEVz/
