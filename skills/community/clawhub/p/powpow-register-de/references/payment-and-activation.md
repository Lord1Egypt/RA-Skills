# Abo-Aktivierung und Zahlung — powpow-register

## Fazit (zuerst die Antwort)
> **Kostenlose Testphase (ab 2026-10-18; das tatsächliche Verhalten der Plattform gilt)**: in dieser Phase kann ein registriertes Konto alle Funktionen direkt nutzen, und **ein Abo ist ein optionales Upgrade und keine Voraussetzung** — den Ablauf dieser Datei nur befolgen, wenn die Nutzer:in aktiv Mitgliedschaft möchte. Endet die Testphase, werden nicht abonnierte Konten beim Besuch von Inhaltsseiten auf die Abo-Seite umgeleitet; das Abo einfach nach dieser Datei abschließen.


**Sowohl Alipay- als auch PayPal-Abos kann der agent übernehmen — Bestellung anlegen und Zahlungseingang verfolgen inklusive.**
Alipay ist ein Einmalkauf ohne automatische Verlängerung, für Nutzer:innen in China und mit Alipay; PayPal verlängert sich monatlich automatisch und ist jederzeit kündbar,
für Nutzer:innen im Ausland und ohne Alipay. WeChat-QR (manuelle Bestätigung) und Huawei IAP gibt es weiterhin, sie werden vom Skill aber nicht übernommen.

Die Verantwortlichkeitsgrenze im Zahlschritt: Der agent darf **Bestellungen erstellen, die Kasse öffnen und den Zahlungseingang abfragen**; er kommt **niemals** mit dem Alipay-/PayPal-Konto /
den Zahlungs-Credentials des Nutzers in Berührung und verspricht niemals „Ich zahle für dich". Die Zahlungshandlung führt immer der Nutzer selbst an der offiziellen Kasse aus.

## Alipay-Kanal (vibepay, bevorzugt)

Einmalkauf-Modell: einmal zahlen, die entsprechende Laufzeit wird freigeschaltet, **keine automatische Verlängerung**. Die Pläne sind fest in
`src/lib/alipay-vibepay.ts` hinterlegt (`ALIPAY_PACKAGES`):

| key | planId | Name | Preis | Laufzeit |
|---|---|---|---|---|
| `monthly` | alipay-monthly | Monats-Mitgliedschaft | ¥6.99 | 30 Tage |
| `quarterly` | alipay-quarterly | Quartals-Mitgliedschaft | ¥19.99 | 90 Tage |
| `yearly` | alipay-yearly | Jahres-Mitgliedschaft | ¥69.99 | 365 Tage |

### Endpunkt-Vertrag (vom Skill-Skript bereits gekapselt; der agent baut keine Anfragen selbst)

| Endpunkt | Methode | Beschreibung |
|---|---|---|
| `/api/payment/alipay/create-order` | POST | Benötigt `Authorization: Bearer <JWT>` (ein pending-Nutzer genügt). body `{package}` → Rückgabe `{paymentHtml, outTradeNo, amount, planName}`; `paymentHtml` ist eine Formularseite, die sich automatisch an das Alipay-Gateway absendet |
| `/api/payment/alipay/query` | GET `?outTradeNo=` | Ebenfalls Bearer-Authentifizierung. Rückgabe `paid` / `pending` / `closed` / `unknown` |
| `/api/payment/alipay/notify` | POST (Server-Callback von Alipay) | Prüfung der fünf Signatur-Elemente (Signatur, app_id, Betrag stimmt überein, TRADE_SUCCESS/TRADE_FINISHED, Händler-Eindeutigkeit) → **idempotentes** Aktualisieren der Bestellung + Abo anlegen + Konto aktivieren. Der Skill rührt diesen Endpunkt niemals an |
| `/payment/alipay/return` | Browser-Rückkehrseite | Öffentlicher Pfad; zeigt nach der Zahlung die Bestätigung 「支付成功」 (Zahlung erfolgreich) und pollt innerhalb der Seite den echten Backend-Status |

- Unbezahlte Bestellungen **schließen sich nach 2 Stunden automatisch**; bricht der Nutzer mittendrin ab → einfach erneut `create-order`, um die alte Bestellung braucht man sich nicht zu kümmern.
- Das Skript schreibt `paymentHtml` in eine temporäre HTML-Datei; der agent öffnet sie per Systembefehl, und der Nutzer gelangt direkt in die Alipay-Kasse
  (per QR-Code scannen oder per Alipay-Login zahlen).

### Aktivierungskette (automatisch, kein manueller Schritt nötig)

notify-Signaturprüfung bestanden → `paymentOrders` als bezahlt markiert → `user_subscriptions` anlegen/verlängern
(`planId`, `currentPeriodEnd` werden nach durationDays berechnet; eine Verlängerung rechnet ab dem ursprünglichen Ablaufdatum weiter) →
`users.accountStatus: active` + `subscriptionStatus: ACTIVE` → die Rückkehrseite pollt paid und zeigt den Erfolg an.

### Nach der Zahlung zwingend den Login-Status erneuern (wichtig)

Im JWT steckt der Abo-Anspruch (bei pending-Konten `NONE`). **Der Zahlungseingang aktualisiert nur die Datenbank, nicht das bereits ausgestellte
JWT** — der Anspruch des alten Tokens bleibt weiterhin NONE; damit direkt einen Login-Link zu erzeugen, wirkt wie „kein Mitglied".
Deshalb führt der Skill nach Bestätigung von `paid` / PayPal `ACTIVE` zuerst `refresh-login` aus (erneutes Login für ein neues JWT, der Anspruch wird ACTIVE)
und erzeugt erst danach Link 2. Das ist Design-Verhalten, keine Fehlerbehebung.

## PayPal-Abo-Kanal (vom Skill übernommen; Web, nicht HarmonyOS)

Es gibt nur einen Plan, Premium Monthly (ca. $1/Monat, laut Rückgabe von `/api/subscription/plans`); er **verlängert sich monatlich automatisch**
und der Nutzer kann ihn jederzeit in seinem PayPal-Konto kündigen.

### Endpunkt-Vertrag (vom Skill-Skript gekapselt; der agent baut keine Anfragen selbst)

| Endpunkt | Methode | Beschreibung |
|---|---|---|
| `/api/subscription/plans` | GET | Bearer-Auth; liefert die Liste der verfügbaren Pläne (aktuell nur 1) |
| `/api/subscription/create` | POST | Body `{planId}` → liefert `{subscriptionId, approveUrl, status}`; `status` ist meist `APPROVAL_PENDING` |
| `/api/subscription/create` | GET | Bearer-Auth; liefert `{activeSubscription, allSubscriptions}`; der agent pollt `activeSubscription.subscription.status === 'ACTIVE'` |
| `/api/subscription/verify` | POST | Wird von der Erfolgsseite automatisch aufgerufen (mit Cookie); aktiviert direkt über die PayPal-API, wenn der Webhook noch nicht da ist |
| `/subscription/success` | Browser-Rückkehrseite | Landet nach der PayPal-Autorisierung, pollt verify automatisch und springt danach zur Startseite / Ursprungsseite zurück |
| `/subscription/cancel` | Browser-Seite | Landet bei Abbruch oder Fehler; ein neuer Versuch ist möglich |

### Ablauf in Vertretung

```
create-order --provider paypal  # → liefert approveUrl, in lokale HTML-Datei geschrieben
HTML-Datei öffnen               # → der Browser springt zur PayPal-Autorisierungsseite
query (alle 10–15 s)            # → pollen bis ACTIVE
refresh-login                   # → neues JWT holen (Abo-Anspruch ACTIVE)
login-link --target home        # → den endgültigen Login-Link erzeugen
```

- PENDING-Abos, die innerhalb einer Stunde nicht abgeschlossen werden, räumt das Backend automatisch auf; einfach neu starten.
- Wiederholt der Nutzer `create-order`, nutzt das Backend das noch gültige `APPROVAL_PENDING`-Abo wieder und vermeidet so einen 409.
- Wie bei Alipay: Der Zahlungseingang aktualisiert nur die Datenbank, ein altes JWT wird nicht automatisch erneuert — vor dem Senden des Startseiten-Links **muss** `refresh-login` laufen.

## Die vier Kanäle der Abo-Seite

Die Abo-Seite `src/app/(public)/subscription/page.tsx` zeigt je nach Laufzeitumgebung:

| Kanal | Umgebung | Mechanismus | Aktivierung |
|---|---|---|---|
| **Alipay (bevorzugt)** | Web | `AlipayPaymentSection` über die vibepay-Endpunkte (Tabelle oben) | serverseitige automatische Aktivierung über notify, sekundenschnell |
| PayPal-Abo | Web (nicht HarmonyOS) | `/api/subscription/create` → Weiterleitung zur PayPal-Autorisierung; monatliche automatische Verlängerung, jederzeit kündbar (`/api/subscription/manage`) | PayPal Webhook (`BILLING.SUBSCRIPTION.*`) setzt automatisch active |
| WeChat-QR-Abo | Web (nicht HarmonyOS) | unten auf der Seite 「微信扫码订阅」 (WeChat-QR-Abonnement): QR-Code scannen und überweisen | **manuelle Bestätigung**, der Eingang kann sich verzögern; nach der Zahlung nicht vorschnell auf Fehlschlag schließen |
| Huawei-In-App-Kauf | in der HarmonyOS-App | nativ `NativeBridge.purchaseSubscription()` | `/api/subscription/activate-huawei` aktiviert nach Prüfung der Huawei-Bestellung |

PayPal-Pläne und -Preise werden dynamisch aus `/api/subscription/plans` gelesen; fester Text auf der Seite: Auto-renews. Cancel anytime.

## Status und Weiterleitungen

- Alipay bezahlt → die Rückkehrseite zeigt den Erfolg; PayPal erfolgreich → `/subscription/success` → Konto active →
  automatische Rückleitung zur ursprünglichen Seite aus dem `next`-Parameter (ohne Parameter: Startseite).
- Wer bereits abonniert hat und die Abo-Seite erneut besucht → Anzeige "You're All Set!", nach 3 Sekunden automatisch zurück zur Startseite.
- Zahlung fehlgeschlagen/abgebrochen (PayPal) → `/subscription/cancel`; kann neu angestoßen werden.

## Troubleshooting

| Symptom | Behandlung |
|---|---|
| Alipay bezahlt, `query` bleibt trotzdem pending | notify verzögert sich nur äußerst selten; 30 Sekunden warten und erneut abfragen. Klappt es weiterhin: den Nutzer im Browser den Status der Rückkehrseite prüfen lassen; hilft das auch nicht, den Plattform-Support kontaktieren (dongtao@outlook.com) und die `outTradeNo` nennen |
| Alipay bezahlt, aber mit Link 2 weiterhin blockiert | `refresh-login` wurde ausgelassen (der Anspruch des alten JWT ist nicht aktualisiert) — zuerst `refresh-login`, dann `login-link` |
| PayPal-`query` bleibt PENDING | Der Nutzer hat die Autorisierung bei PayPal nicht abgeschlossen; prüfen, ob der Autorisierungslink im Browser geöffnet wurde. Wenn trotz Autorisierung weiter PENDING, kann der Webhook verzögert sein — den Nutzer auf der Erfolgsseite noch einige Sekunden warten oder neu laden lassen |
| PayPal-`query` meldet 409 | Es gibt schon ein unfertiges PENDING-Abo; 1 Stunde warten, bis es abläuft, oder die Autorisierung des alten Links im Browser abschließen |
| PayPal bezahlt, aber mit Link 2 weiterhin blockiert | Wie bei Alipay: zuerst `refresh-login`, dann `login-link` |
| Nach der Zahlung weiterhin 403 (PayPal) | Webhooks verzögern sich gelegentlich; neu einloggen und den Status auffrischen |
| Mit WeChat bezahlt, aber nicht freigeschaltet | Die manuelle Bestätigung läuft asynchron; erst nach mehreren Stunden ohne Freischaltung den Plattform-Support kontaktieren |
| Die Abo-Seite meldet "No subscription plans available" | `/api/subscription/plans` hat keine verfügbaren PayPal-Pläne — Konfigurationsproblem auf Plattformseite; Nutzer in Festlandchina nehmen einfach den Alipay-Weg |

## Historische Anmerkung

Im Code existiert außerdem ein **alter** Alipay-Web-Zahlungsweg (`src/lib/alipay.ts`, `/api/payment/create-order`,
¥9.90/¥99 Einmalkauf; ohne konfigurierte Sandbox-Keys Rückfall auf eine simulierte Zahlung); er wurde nie in die Abo-Seiten-UI integriert und hat mit vibepay
nichts zu tun. Der Skill rührt ihn grundsätzlich nicht an; `alipay-vibepay.ts` ist der aktuell gültige Kanal.
