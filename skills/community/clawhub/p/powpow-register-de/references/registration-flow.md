# Registrierungsablauf im Detail — powpow-register

Zum Nachschlagen bei der Fehlerbehebung. Alle Regeln stammen aus dem Plattform-Quellcode (Next.js — Frontend und Backend validieren konsistent); die Quellen sind angegeben.
Bei Plattform-Updates zählt das tatsächliche Online-Verhalten.

## Einstiege

- Registrierungsseite: https://global.powpow.online/register
- Login-Seite: https://global.powpow.online/login
- Abo-Seite: https://global.powpow.online/subscription
- Wer über einen Share-Link o. Ä. mit `?next=...` hereinkommt, wird nach Registrierung + Zahlung automatisch zur ursprünglichen Seite zurückgeleitet.

## Formularfelder und Regeln

| Feld | Pflicht | Regeln | Quellcode-Stelle |
|---|---|---|---|
| Avatar | optional | Bild ≤5 MB, SVG wird nicht unterstützt; serverseitige automatische Komprimierung (>100 KB: auf 400×400 / Qualität 90 komprimiert) | `src/app/api/auth/register/route.ts` |
| Benutzername | Pflicht | 2–50 Zeichen; nach trim **kleingeschrieben** gespeichert (Tom und tom gelten als derselbe Benutzername; Registrierungs- wie Login-Seite sind case-insensitiv) | wie oben (zod schema) |
| Passwort | Pflicht | 8–100 Zeichen; muss Großbuchstaben, Kleinbuchstaben und Zahlen zugleich enthalten | wie oben |
| Passwort bestätigen | Pflicht | muss mit dem Passwort übereinstimmen (nur Frontend-Prüfung) | `src/app/(public)/register/page.tsx` |
| Spitzname | optional | ≤100 Zeichen; wenn nicht ausgefüllt, wird standardmäßig der Benutzername genommen | register route |
| E-Mail | **Pflicht** | gültiges E-Mail-Format, ≤255 Zeichen; mit einer E-Mail kann nur ein Konto registriert werden | register route |
| E-Mail-Verifizierungscode | **Pflicht** | 6-stellige Zahl; **10 Minuten gültig**; wird bei erfolgreicher Prüfung sofort ungültig; beim erneuten Senden wird der alte Code als verwendet markiert | `src/lib/email-verification.ts` |
| Telefonnummer | optional | Festlandchina-Nummer: beginnt mit `1[3-9]`, insgesamt 11 Stellen; eine Telefonnummer lässt sich nur an ein Konto binden | register route |

Die Seite bietet außerdem drei Drittanbieter-Login-Buttons: **Google, Watcha, Huawei-Konto** (`GoogleSignInButton` /
`WatchaLoginButton` / `HuaweiLoginButton`). Drittanbieter-Konten haben kein lokales Passwort; ein späterer Login per Passwort liefert
「该账号未设置密码，请使用其他方式登录」 (Für dieses Konto ist kein Passwort festgelegt; bitte melde dich auf andere Weise an).

## Rate-Limit- und Brute-Force-Schutz-Parameter

| Aktion | Limit | Quelle |
|---|---|---|
| Registrierung absenden | **3 mal/Minute/IP**, darüber 429 | `src/lib/rate-limit.ts` `REGISTER_RATE_LIMIT` |
| Verifizierungscode senden | pro IP 1 mal/Minute **und** pro E-Mail 1 mal/Minute, darüber 429; Frontend-Button mit 60-Sekunden-Countdown | `src/app/api/auth/register/send-code/route.ts` |
| Verifizierungscode prüfen | pro E-Mail höchstens **5 Versuche** innerhalb von 10 Minuten; am Limit wird selbst bei richtigem Code abgelehnt — der Code muss neu angefordert werden | `src/lib/email-verification.ts` |
| Code bei vergessenem Passwort | 1 mal/Minute/IP | `src/app/api/auth/forgot-password/route.ts` |
| Login | 5 mal/Minute/IP; dasselbe Konto nach **5 Fehlversuchen in Folge 30 Minuten gesperrt** (423), mit Anzeige der abnehmenden Restversuche | `src/app/api/auth/login/route.ts`, `rate-limit.ts` |

**Privacy-Verhalten**: Beim Senden des Verifizierungscodes / bei vergessenem Passwort geben die Endpunkte — ob die E-Mail bereits registriert ist oder nicht existiert —
einheitlich eine Erfolgsmeldung zurück und verraten nicht, ob die E-Mail bereits registriert ist.

## Gleichwertigkeit von Agent-Durchführungsmodus und Web-Registrierung

Das Skill-Skript ruft **dieselben öffentlichen APIs** auf (`/api/auth/register`, `send-code`, `login`,
`/api/auth/me`) und durchläuft damit exakt dieselben Prüf-, Rate-Limit- und Fehlerpfade wie das Absenden des Registrierungsformulars — alle Regeln dieser
Datei gelten für beide Modi gleichermaßen. Skript-Sequenz und Befehls-Vertrag siehe `references/agent-flow.md`.

## Statusfluss nach erfolgreicher Registrierung

> **Kostenlose Testphase (ab 2026-10-18; das tatsächliche Verhalten der Plattform gilt)**: ein neu registriertes Konto kann **alle Funktionen direkt nutzen**
> (Feed, Karte, digitale Menschen, Check-ins usw.), keine Zahlung nötig; nicht abonnierte Konten werden von Inhaltsseiten nicht mehr blockiert. Die Beschreibung der
> „pending-Blockierung“ in diesem Abschnitt ist der normale Zustand nach Ende der Testphase — ist es so weit, gilt das tatsächliche Online-Verhalten.

1. Die Nutzer:in wird mit `accountStatus: 'pending'` gespeichert, mit initial **3 Badges** (register route).
2. Der Server setzt zudem zwei HttpOnly-Cookies: das JWT (kann Seiten direkt aufrufen) und
   das pendingUserToken (Identitätsnachweis für den Abo-Ablauf).
3. Im normalen Zustand (Testphase beendet / keine kostenlose Phase) erkennt die Registrierungsseite `pending_payment` → Weiterleitung zu `/subscription`
   (unter Beibehaltung des `next`-Rückkehrparameters); im agent-übernommenen Modus erreicht `me?token=…&redirect=/subscription` denselben Effekt.
   **In der kostenlosen Testphase wird dieser Schritt nicht ausgelöst** — nach der Registrierung direkt auf die Startseite und loslegen.
4. Zahlung abgeschlossen → `accountStatus` wird `active` (**Alipay aktiviert automatisch serverseitig via notify**;
   PayPal aktiviert via Webhook; WeChat-QR-Code wird manuell bestätigt; Huawei IAP läuft über `activate-huawei`).
   Details in `payment-and-activation.md`.

Im normalen Zustand erhalten inaktive (pending) Nutzer:innen beim Aufruf der Kern-APIs (Feed, Karte, Digital-Mensch-Chat, Check-ins usw.) 403;
geteilte Beitrags-Links sind die Ausnahme (bleiben öffentlich zugänglich). In der kostenlosen Testphase ist diese Blockierung ausgesetzt und alles ist offen.
## Troubleshooting-Tabelle häufiger Fehler

| Symptom | Ursache | Was tun |
|---|---|---|
| 「用户名已存在」 (Der Benutzername existiert bereits) | Benutzername vergeben (case-insensitiv) | einen anderen Benutzernamen wählen |
| 「邮箱已被使用」 (Die E-Mail ist bereits in Verwendung) | E-Mail schon registriert | E-Mail wechseln; oder stattdessen Login + 「忘记密码」 (Passwort vergessen), um das alte Konto zurückzuholen |
| 「邮箱验证码错误或已过期」 (Der E-Mail-Verifizierungscode ist falsch oder abgelaufen) | Code falsch eingegeben / älter als 10 Minuten / nach mehr als 5 Fehlversuchen abgelehnt | 「重新发送」 (Erneut senden) anklicken und den Code aus der **neuesten** E-Mail verwenden |
| Verifizierungscode kommt nicht an | 60-Sekunden-Rate-Limit; oder im Spam-/Werbungsordner gelandet | Countdown abwarten und erneut senden; Spam-Ordner durchforsten |
| 「手机号已被使用」 (Die Telefonnummer ist bereits in Verwendung) | Telefonnummer bereits an ein anderes Konto gebunden | Telefonnummer weglassen (optional) oder Nummer wechseln |
| 「注册请求过于频繁」 (Registrierungsanfragen zu häufig) / 429 | Registrierungslimit 3 mal/Minute/IP erreicht | ein paar Minuten warten und erneut versuchen |
| 409 「用户名或邮箱已被注册」 (Benutzername oder E-Mail bereits registriert) | beim Absenden zeitgleich mit jemand anderem kollidiert (Concurrency-Fallback) | Benutzername oder E-Mail ändern und erneut versuchen |
| 「图片大小不能超过5MB」 (Das Bild darf 5 MB nicht überschreiten) / 「不支持 SVG」 (SVG wird nicht unterstützt) | Avatar regelwidrig | Bild wechseln oder Avatar überspringen |
| Nutzer:in öffnet den Login-Link, landet aber auf der Abo-Seite (statt der Startseite) | Die kostenlose Testphase ist beendet und die Paywall der Plattform ist zurück | Den Abo-Zahlungsablauf aus Schritt 7 in SKILL.md befolgen; nach dem Abo `refresh-login` ausführen und dann den Startseiten-Link senden |
| Registrierung erfolgreich, aber Login gibt 403 „请完成订阅以激活账户“ | Das Konto ist noch pending, und die Plattform ist nicht in einer kostenlosen Testphase (erwarteter Zustand vor der Zahlung) | Tritt in der kostenlosen Testphase nicht auf; falls doch, ist die Testphase beendet — zuerst das Abo abschließen; nach Zahlung weiterhin 403: ein altes JWT wurde verwendet — im Skript-Modus zuerst `refresh-login` ausführen, um gegen einen neuen Login-Status zu tauschen |
| Login 423 「账户已锁定」 (Das Konto ist gesperrt) | 5× in Folge ein falsches Passwort | 30 Minuten warten |
| Login 401 「还剩 N 次尝试机会」 (Noch N Versuche übrig) | falsches Passwort, kurz vor der Sperre | in Ruhe nochmal versuchen — oder direkt über 「忘记密码」 (Passwort vergessen) gehen |
| 「该账号未设置密码，请使用其他方式登录」 (Für dieses Konto ist kein Passwort festgelegt; bitte melde dich auf andere Weise an) | Drittanbieter-Konto (Google/Watcha/Huawei) | mit dem ursprünglichen Drittanbieter-Button einloggen |
| 「该账号已注销」 (Dieses Konto wurde deaktiviert) | Konto wurde deaktiviert (deactivate) | erneut registrieren |

## Login-Wissenswertes (für die gelegentliche Fehlersuche)

Der Login akzeptiert **Benutzername / E-Mail / Telefonnummer** als kombinierte Eingabe (jede der drei Angaben taugt als Kontoname).
Passwort vergessen: Login-Seite → 「忘记密码」 (Passwort vergessen) → Registrierungs-E-Mail eingeben, den 6-stelligen Code empfangen → zurücksetzen.
