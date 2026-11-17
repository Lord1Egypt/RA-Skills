# Der Starter

Ein Nutzer, der eine Kommandozeile öffnen muss, benutzt das Werkzeug nicht.
Fertige Vorlagen liegen in `scripts/starter/`; hier steht, warum sie so
aussehen, wie sie aussehen.

## Was ein Starter leisten muss

Das Starten selbst ist eine Zeile. Der Aufwand steckt in den vier Fällen, in
denen es schiefgeht — und jeder braucht eine Antwort, die dem Nutzer sagt, was
er tun soll.

### 1. Laufzeit fehlt

Nicht „Python nicht gefunden" — das weiß der Nutzer dann auch. Sondern:

```
Python wurde nicht gefunden.
Herunterladen: https://www.python.org/downloads/
Beim Installieren "Add python.exe to PATH" ankreuzen — ohne
diesen Haken findet der Starter Python spaeter nicht.
```

Der Haken ist der eigentliche Punkt. Er ist im Installationsprogramm klein,
unten links, und standardmäßig aus. Wer ihn übersieht, installiert Python
erfolgreich und bekommt trotzdem dieselbe Meldung.

Reihenfolge unter Windows: `py -3`, dann `python`, dann `python3`. Der
`py`-Starter ist am zuverlässigsten und umgeht den Store-Platzhalter, den
Windows sonst unter `python` anbietet.

### 2. Läuft schon

Zweiter Doppelklick darf keinen zweiten Prozess starten — sonst kämpfen zwei
um denselben Port und einer stirbt mit einer Fehlermeldung, die niemand liest.

Erst den Gesundheitspfad anfragen. Antwortet er, nur das Fenster öffnen.

### 3. Port antwortet nicht

`sleep 3` ist geraten. Auf einem langsamen Rechner oder beim ersten Start nach
einem Update dauert es länger, und der Nutzer sieht „nicht erreichbar".

```powershell
foreach ($i in 1..40) {                 # bis zu 20 Sekunden
  Start-Sleep -Milliseconds 500
  if (Test-Alive)      { $ok = $true; break }
  if ($proc.HasExited) { break }        # nicht auf einen toten Prozess warten
}
```

Die zweite Bedingung ist wichtig: Ohne sie wartet der Nutzer die vollen
20 Sekunden auf etwas, das nach 200 ms abgestürzt ist.

### 4. Programm bricht sofort ab

Ein Fenster, das aufgeht und sofort wieder zu ist, ist die schlimmste aller
Rückmeldungen. Ausgabe deshalb in eine Datei umleiten und beim Scheitern die
letzten Zeilen zeigen:

```powershell
Get-Content "$LogFile.err" -Tail 15 | ForEach-Object { Write-Host "    $_" }
Write-Host '  Nochmal mit sichtbarem Fenster:  .\start.ps1 -Console'
```

## Drei Dateien nebeneinander

| Datei | wofür |
|---|---|
| `Start.cmd` | der Normalfall |
| `Beenden.cmd` | ohne das sucht der Nutzer im Task-Manager |
| `Fehlersuche.cmd` | sichtbares Fenster, wenn etwas klemmt |

Sprechende Dateinamen. `run.cmd` sagt nichts.

## Windows: Ausführungsrichtlinie

PowerShell-Dateien lassen sich standardmäßig nicht doppelklicken. Deshalb der
Umweg über eine `.cmd`:

```bat
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start.ps1" %*
```

`-ExecutionPolicy Bypass` gilt nur für diesen einen Aufruf und ändert nichts
an den Einstellungen des Rechners. Das ist erwähnenswert, weil manche Nutzer
bei „Bypass" zu Recht stutzen — schreib es in die Datei und ins README.

`%~dp0` ist der Ordner der Datei mit Schrägstrich am Ende. Ohne ihn läuft das
Skript im Arbeitsverzeichnis der Verknüpfung, was selten das richtige ist.

## Als eigenes Fenster öffnen

```powershell
Start-Process $edge "--app=$Url"
```

Ohne Adressleiste und Lesezeichenleiste wirkt es wie ein Programm. Pfade:

```powershell
$edge   = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
$chrome = "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe"
```

Die geschweiften Klammern sind nötig. `"$env:ProgramFiles(x86)\…"` endet nach
`ProgramFiles`; das `(x86)` wird zu gewöhnlichem Text, und der Pfad stimmt
nicht mehr. Der Fehler fällt nicht auf, weil danach der Rückfall auf den
Standardbrowser greift — es geht ja irgendwie.

## macOS und Linux

Gleiche Logik, andere Werkzeuge:

- Hintergrund: `nohup … &` und die Prozessnummer in eine Datei
- Warten: `curl -sf --max-time 2` in einer Schleife
- Öffnen: `open` unter macOS, `xdg-open` unter Linux
- Ausführbar machen: `chmod +x start.sh` — sonst ist der Doppelklick wirkungslos

Unter macOS lässt sich eine `.command`-Datei doppelklicken; sie ist eine
gewöhnliche Shell-Datei mit dieser Endung.

## Dauerhaft mitlaufen lassen

Nur anbieten, wenn der Nutzer danach fragt — ungefragter Autostart ist ein
Übergriff.

- **Windows**: Verknüpfung in `shell:startup`, oder Aufgabenplanung mit
  Auslöser „bei Anmeldung"
- **macOS**: `launchd`-Datei unter `~/Library/LaunchAgents/`
- **Linux**: `systemd --user` mit `WantedBy=default.target`

In allen drei Fällen ohne Browserfenster starten (`-NoBrowser`), sonst springt
bei jeder Anmeldung ein Fenster auf.
