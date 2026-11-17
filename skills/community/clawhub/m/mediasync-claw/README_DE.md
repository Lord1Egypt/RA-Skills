<div align="center">

# MediaSync-Claw: Remote P2P-Medienserver & Streaming-Skill für OpenClaw

[English](README.md) | [简体中文](README_ZH.md) | [日本語](README_JA.md) | [Deutsch](README_DE.md) | [Español](README_ES.md)

</div>

---

## 📖 Übersicht & Kernfunktionalität

**MediaSync-Claw** ist ein dedizierter **OpenClaw-Skill** und **P2P-Medienserver** für das persönliche Video- und Audiostreaming im Homelab- und Self-Hosted-Bereich.

Über die Anbindung von OpenClaw an WhatsApp können Sie jederzeit und von überall auf die Medienbibliothek Ihres lokalen Heim-PCs zugreifen. Die generierte Medienliste ermöglicht ein schnelles, verlustfreies P2P-Streaming über den **AIpollo Player**.

---

## ⚙️ Systemanforderungen

* **OpenClaw**: OpenClaw ist lokal installiert und einsatzbereit.
* **Firewall- / Antivirus-Freigabe**: Fügen Sie `frpc.exe` als Ausnahme in Windows Defender oder Ihrer Sicherheitssoftware hinzu. *Wir garantieren, dass `frpc.exe` absolut sicher und ungepatcht ist.*

---

## 🚀 Schritt-für-Schritt Installationsanleitung

1. **Download & Installation**: Klonen oder laden Sie dieses Repository in das Skills-Verzeichnis von OpenClaw herunter.
2. **Medienordner anlegen**: Erstellen Sie im Skill-Verzeichnis einen Ordner namens `videos` und hinterlegen Sie dort die MP4-Videodateien.
3. **WhatsApp konfigurieren**: Richten Sie die WhatsApp-Schnittstelle in OpenClaw ein.
4. **Skill ausführen**: Starten Sie den MediaSync-Claw-Skill in OpenClaw.
5. **Fernsteuerung via WhatsApp**: Senden Sie einen Befehl über WhatsApp (z. B. wenn Sie Videos auflisten, suchen oder abspielen möchten), um die Medienliste abzurufen.
6. **Wiedergabe starten**: Klicken Sie auf den generierten Link in der Medienliste, um den Stream im AIpollo Player zu starten.

---

## 🔒 Sicherheits- und Risikohinweise

### Risiko 1: Öffentlicher Netzwerkzugriff via FRP-Reverse-Proxy
Um Medien hinter NAT-Routern und Firewalls erreichbar zu machen, baut der FRP-Client (`frpc`) einen ausgehenden Tunnel zu einem Relay-Server (`frps`) auf. Dadurch wird der lokale Dienst über die Domain `*.yunfrp.net` erreichbar.

### Risiko 2: HTTP-Klartextübertragung & P2P-Streaming
Das eigentliche Videostreaming erfolgt über eine **direkte P2P-Verbindung**. Über HTTP werden ausschließlich Steuerbefehle übertragen; es werden keine sensiblen Benutzerdaten übertragen.

### Risiko 3: Bezug der ausführbaren Datei `frpc.exe`
Um die Integrität der Lieferkette zu gewährleisten, wird die Binärdatei `frpc.exe` direkt aus den offiziellen GitHub-Releases bezogen.

---

## 🛡️ Sicherheitsempfehlungen

* **Dedizierte Hardware / Virtuelle Maschine**: Für maximale Sicherheit empfehlen wir, diesen Dienst auf einem separaten Server (z. B. Homelab/NAS) oder in einer isolierten virtuellen Maschine (VM) zu betreiben.
* **Regelmäßige Updates**: Halten Sie Ihr Betriebssystem und Ihre OpenClaw-Umgebung stets auf dem neuesten Stand.

---

## 💻 Plattformkompatibilität

* **Aktuell unterstützt**: Windows (x64)
* **In Entwicklung**: Linux / macOS Support folgt in Kürze.

*Bei Fragen oder Problemen öffnen Sie bitte ein GitHub-Issue. Vielen Dank für Ihr Vertrauen!*