# Example Conversations

Illustrative dialogues showing intended agent behaviour (safety tiers, formatting, workflows).

## Tier 0 — instant read

> **User:** Wie viele Geräte haben wir insgesamt?
> **Agent:** 127 Geräte: 89 Windows, 22 iOS, 12 Android, 4 macOS.

## Tier 1 — quick confirm

> **User:** Sync den Laptop von Max Müller
> **Agent:** Gefunden: MAX-LAPTOP (Windows 11, zuletzt gesynct vor 4 Tagen). Soll ich den Sync anstoßen?
> **User:** ja
> **Agent:** ✅ Sync-Befehl an MAX-LAPTOP gesendet.

## Tier 2 — change summary + confirm

> **User:** Erstell eine Compliance Policy für Windows mit BitLocker-Pflicht
> **Agent:** Vorschlag: **"Windows – BitLocker Pflicht"** · Plattform Windows 10/11 · Anforderung: BitLocker aktiviert · Aktion bei Nichteinhaltung: als non-compliant markieren (sofort). Noch keine Gruppe zugewiesen. Soll ich die Policy so erstellen?
> **User:** ja
> **Agent:** ✅ Erstellt (ID …). Soll ich sie einer Gruppe zuweisen?

## Tier 3 — type-back confirmation

> **User:** Wipe MAX-LAPTOP
> **Agent:** ⚠️ Das setzt **MAX-LAPTOP** (Windows 11, Benutzer max.mueller@…) vollständig auf Werkseinstellungen zurück. Alle Daten gehen verloren, das Gerät muss neu enrollt werden. Tippe zur Bestätigung den Gerätenamen exakt ein.
> **User:** MAX-LAPTOP
> **Agent:** ✅ Wipe-Befehl gesendet. Status siehst du unter Geräteaktionen; das Gerät verschwindet nach Abschluss aus Intune.

## Read-only mode

> **User:** Lösch die alte Test-Policy
> **Agent:** Ich bin im Read-Only-Modus (INTUNE_READ_ONLY=true) und kann keine Änderungen vornehmen. Die Policy "Test-Policy" (zuletzt geändert 2026-03-01, 0 Zuweisungen) kannst du im Portal löschen — oder deaktiviere den Read-Only-Modus.

## Multi-step workflow

> **User:** Offboarde alle Geräte von Frau Weber
> **Agent:** Anna Weber hat 2 Geräte: WEBER-NB01 (Windows) und iPhone-AW (iOS). Plan: 1) beide Geräte retiren (Firmendaten entfernen) oder wipen — was möchtest du? 2) Autopilot-Eintrag von WEBER-NB01 löschen, falls die Hardware das Unternehmen verlässt. 3) Anna aus den Gruppen "Intune-Users" und "VPN-Access" entfernen — jede Gruppenentfernung bestätige ich einzeln mit dir (Tier 2).
