# 🛒 Knuspr CLI

> **⚠️ Hobby-Projekt Disclaimer**
> 
> Dies ist ein privates Hobby-Projekt und steht in keiner Verbindung zu Knuspr/Rohlik.
> Die CLI nutzt keine offizielle API — Änderungen seitens Knuspr können jederzeit zu
> Funktionseinschränkungen führen. Nutzung auf eigene Verantwortung.

REST-ähnliche, AI-Agent-freundliche CLI für [Knuspr.de](https://www.knuspr.de).

Einkaufen, Suchen, Warenkorb verwalten, Lieferzeiten, Bestellhistorie — alles vom Terminal aus.

## ✨ Features

- 🔐 **Authentifizierung** — Sichere Session-Speicherung
- 🔍 **Produktsuche** — Mit Filtern (Bio, Favoriten, Rette Lebensmittel)
- 🛒 **Warenkorb** — Anzeigen, hinzufügen, entfernen, leeren
- 📅 **Lieferzeitfenster** — Anzeigen und reservieren
- 📋 **Bestellhistorie** — Ansehen und wiederholen
- ⭐ **Favoriten** — Verwalten
- 🥬 **Rette Lebensmittel** — Reduzierte Produkte kurz vor Ablauf
- 📊 **JSON-Output** — Für Automatisierung und AI-Agents
- 🐚 **Shell-Completion** — Bash, Zsh, Fish

## 📦 Installation

```bash
# Repository klonen
git clone https://github.com/Lars147/knuspr-cli.git
cd knuspr-cli

# Ausführbar machen
chmod +x knuspr_cli.py

# Option A: Alias setzen (in ~/.bashrc oder ~/.zshrc)
alias knuspr="python3 /pfad/zu/knuspr_cli.py"

# Option B: Ins PATH kopieren
sudo cp knuspr_cli.py /usr/local/bin/knuspr
```

**Voraussetzungen:** Python 3.8+ (keine externen Dependencies!)

## 🏗️ Command-Struktur

Die CLI folgt einem REST-ähnlichen Pattern: `knuspr <ressource> <aktion>`

```
knuspr
├── auth        Authentifizierung
│   ├── login       Bei Knuspr.de einloggen
│   ├── logout      Ausloggen und Session löschen
│   └── status      Login-Status anzeigen
│
├── config      Konfiguration
│   ├── show        Konfiguration anzeigen
│   ├── set         Präferenzen interaktiv setzen
│   └── reset       Zurücksetzen
│
├── account     Account-Informationen
│   └── show        Premium-Status, Mehrwegtaschen, etc.
│
├── product     Produkte
│   ├── search      Produkte suchen
│   ├── show        Produkt-Details anzeigen
│   ├── filters     Verfügbare Filter anzeigen
│   └── rette       Rette Lebensmittel anzeigen
│
├── favorite    Favoriten
│   ├── list        Alle Favoriten anzeigen
│   ├── add         Produkt zu Favoriten hinzufügen
│   └── remove      Produkt aus Favoriten entfernen
│
├── cart        Warenkorb
│   ├── show        Warenkorb anzeigen
│   ├── add         Produkt hinzufügen
│   ├── remove      Produkt entfernen
│   ├── clear       Warenkorb leeren
│   └── open        Im Browser öffnen
│
├── slot        Lieferzeitfenster
│   ├── list        Verfügbare Zeitfenster anzeigen
│   ├── reserve     Zeitfenster reservieren
│   ├── release     Reservierung stornieren
│   └── current     Aktuelle Reservierung anzeigen
│
├── order       Bestellungen
│   ├── list        Bestellhistorie anzeigen
│   ├── show        Details einer Bestellung
│   └── repeat      Bestellung wiederholen (in Warenkorb)
│
├── insight     Einkaufs-Insights
│   ├── frequent    Häufig gekaufte Produkte
│   └── meals       Mahlzeitvorschläge (breakfast, lunch, etc.)
│
├── delivery    Lieferinformationen
│   └── show        Liefergebühren & bevorstehende Lieferungen
│
└── completion  Shell-Completion
    ├── bash        Bash Completion ausgeben
    ├── zsh         Zsh Completion ausgeben
    └── fish        Fish Completion ausgeben
```

## 🚀 Schnellstart

```bash
# 1. Einloggen
knuspr auth login

# 2. Produkte suchen
knuspr product search "Milch"

# 3. Produkt zum Warenkorb hinzufügen (ID aus Suche)
knuspr cart add 11943

# 4. Warenkorb prüfen
knuspr cart show

# 5. Lieferzeitfenster anzeigen
knuspr slot list

# 6. Slot reservieren (ID aus Liste)
knuspr slot reserve 110425

# 7. Im Browser zur Kasse
knuspr cart open
```

## 📖 Befehle im Detail

### 🔐 auth — Authentifizierung

```bash
knuspr auth login                              # Interaktiv einloggen
knuspr auth login -e user@mail.de -p geheim    # Mit Credentials
knuspr auth logout                             # Session löschen
knuspr auth status                             # Login-Status anzeigen
knuspr auth                                    # Default: status
```

### ⚙️ config — Konfiguration

```bash
knuspr config show                   # Aktuelle Konfiguration anzeigen
knuspr config set                    # Präferenzen interaktiv setzen
knuspr config reset                  # Konfiguration zurücksetzen
knuspr config                        # Default: show
```

**Konfigurierbare Präferenzen:**
- 🌿 Bio-Produkte bevorzugen
- 📊 Standard-Sortierung (Relevanz, Preis, Bewertung)
- 🚫 Ausschlüsse (z.B. "Laktose", "Gluten", "Schwein")

### 👤 account — Account-Informationen

```bash
knuspr account show                  # Premium-Status, Mehrwegtaschen, etc.
knuspr account                       # Default: show
```

### 📦 product — Produkte

```bash
# Suchen
knuspr product search "Milch"                  # Einfache Suche
knuspr product search "Käse" -n 20             # Max. 20 Ergebnisse
knuspr product search "Tofu" --bio             # Nur Bio-Produkte
knuspr product search "Brot" --favorites       # Nur Favoriten
knuspr product search "Joghurt" --rette        # Nur Rette Lebensmittel
knuspr product search "Wurst" --exclude Schwein  # Begriffe ausschließen

# Sortierung
knuspr product search "Milch" --sort price_asc   # Günstigste zuerst
knuspr product search "Milch" --sort price_desc  # Teuerste zuerst

# Produkt-Details
knuspr product show 11943                      # Details zu Produkt-ID

# Verfügbare Filter
knuspr product filters "Milch"                 # Filter-Optionen anzeigen

# Rette Lebensmittel (reduziert, kurz vor Ablauf)
knuspr product rette                           # Alle anzeigen
knuspr product rette "Fleisch"                 # Nach Begriff filtern
knuspr product rette -n 10                     # Max. 10 Ergebnisse
```

### ⭐ favorite — Favoriten

```bash
knuspr favorite list                 # Alle Favoriten anzeigen
knuspr favorite list -n 20           # Max. 20 anzeigen
knuspr favorite add 11943            # Produkt zu Favoriten
knuspr favorite remove 11943         # Aus Favoriten entfernen
knuspr favorite                      # Default: list
```

### 🛒 cart — Warenkorb

```bash
knuspr cart show                     # Warenkorb anzeigen
knuspr cart add 11943                # 1× Produkt hinzufügen
knuspr cart add 11943 -q 3           # 3× Produkt hinzufügen
knuspr cart remove 11943             # Produkt entfernen
knuspr cart clear                    # Kompletten Warenkorb leeren
knuspr cart open                     # Warenkorb im Browser öffnen
knuspr cart                          # Default: show
```

### 📅 slot — Lieferzeitfenster

```bash
knuspr slot list                     # Verfügbare Zeitfenster
knuspr slot list -n 7                # Mehr Tage anzeigen
knuspr slot list --detailed          # Mit 15-Min-Slots und IDs

knuspr slot reserve 110425           # Slot reservieren (15-Min-Präzision)
knuspr slot reserve 110425 --type VIRTUAL  # 1-Stunden-Fenster

knuspr slot current                  # Aktuelle Reservierung anzeigen
knuspr slot release                  # Reservierung stornieren
knuspr slot                          # Default: list
```

### 📋 order — Bestellungen

```bash
knuspr order list                    # Bestellhistorie
knuspr order list -n 20              # Mehr Bestellungen anzeigen
knuspr order show 1011234895         # Details einer Bestellung
knuspr order repeat 1011234895       # Alle Produkte in Warenkorb legen
knuspr order                         # Default: list
```

### 📊 insight — Einkaufs-Insights

```bash
# Häufig gekaufte Produkte
knuspr insight frequent              # Top 10 aus letzten 5 Bestellungen
knuspr insight frequent -n 20        # Top 20 anzeigen
knuspr insight frequent -o 10        # Mehr Bestellungen analysieren

# Mahlzeitvorschläge basierend auf Kaufhistorie
knuspr insight meals breakfast       # Frühstücks-Produkte
knuspr insight meals lunch           # Mittagessen
knuspr insight meals dinner          # Abendessen
knuspr insight meals snack           # Snacks
knuspr insight meals baking          # Backzutaten
knuspr insight meals drinks          # Getränke
knuspr insight meals healthy         # Gesunde Produkte

knuspr insight                       # Default: frequent
```

### 🚚 delivery — Lieferinformationen

```bash
knuspr delivery show                 # Liefergebühren, bevorstehende Bestellungen
knuspr delivery                      # Default: show
```

### 🐚 completion — Shell-Completion

```bash
# Bash (in ~/.bashrc einfügen)
knuspr completion bash >> ~/.bashrc
source ~/.bashrc

# Zsh (in ~/.zshrc einfügen)
knuspr completion zsh >> ~/.zshrc
source ~/.zshrc

# Fish
knuspr completion fish > ~/.config/fish/completions/knuspr.fish
```

## 📊 JSON-Ausgabe

Alle Befehle unterstützen `--json` für maschinenlesbare Ausgabe:

```bash
knuspr auth status --json
knuspr product search "Milch" --json
knuspr cart show --json
knuspr order list --json
knuspr slot list --json
```

## 🔑 Credentials einrichten

### Option 1: Interaktiv (empfohlen)

```bash
knuspr auth login
# → E-Mail und Passwort werden abgefragt
```

### Option 2: Umgebungsvariablen

```bash
export KNUSPR_EMAIL="user@example.com"
export KNUSPR_PASSWORD="geheim"
knuspr auth login
```

### Option 3: Credentials-Datei

```bash
cat > ~/.knuspr_credentials.json << 'EOF'
{
  "email": "user@example.com",
  "password": "geheim"
}
EOF
chmod 600 ~/.knuspr_credentials.json
knuspr auth login
```

## 🤖 Beispiele für AI-Agents

```bash
# Produkt-ID aus Suche extrahieren
knuspr product search "Bio Hafermilch" --json | jq '.[0].id'

# Erstes Suchergebnis zum Warenkorb hinzufügen
knuspr cart add $(knuspr product search "Bio Hafermilch" --json | jq -r '.[0].id')

# Warenkorb-Summe auslesen
knuspr cart show --json | jq '.total_price'

# Nächsten verfügbaren Slot finden und reservieren
knuspr slot list --detailed --json | jq '.[0].availabilityDays[0].slots | to_entries[0].value[0].slotId'

# Letzte Bestellung wiederholen
knuspr order repeat $(knuspr order list --json | jq -r '.[0].id')

# Alle Rette-Lebensmittel mit >40% Rabatt
knuspr product rette --json | jq '[.[] | select(.discount | test("-[4-9][0-9]"))]'

# Häufig gekaufte Produkte als Einkaufsliste
knuspr insight frequent --json | jq '.top_items | .[].product_name'

# Frühstücks-Empfehlungen basierend auf Kaufhistorie
knuspr insight meals breakfast --json | jq '.suggestions[:5]'
```

## 🔢 Exit-Codes

| Code | Bedeutung |
|------|-----------|
| `0`  | ✅ Erfolg |
| `1`  | ❌ Allgemeiner Fehler |
| `2`  | 🔐 Authentifizierungsfehler |

## 📁 Dateien

| Datei | Beschreibung |
|-------|--------------|
| `~/.knuspr_session.json` | Session-Cookies (automatisch verwaltet) |
| `~/.knuspr_credentials.json` | Gespeicherte Login-Daten (optional) |
| `~/.knuspr_config.json` | Benutzer-Präferenzen |

## 🛠️ Abhängigkeiten

**Keine!** Nur Python 3.8+ und die Standardbibliothek.

## 📜 Lizenz

MIT

## 👤 Autor

Lars Heinen

---

> 💡 **Tipp:** Nutze `knuspr <command> --help` für detaillierte Hilfe zu jedem Befehl.
