# Stil-Layer: Basis

> Standard-Humanisierung ohne besonderen Stil.
> Funktioniert für jeden deutschen Text. Neutral, klar, menschlich.
> Dieser Layer wird angewendet wenn der Benutzer "Humanisiere das" oder "Mach das menschlicher" sagt.

---

## Prinzip

Der Basis-Layer macht genau drei Dinge:
1. **Entfernen:** KI-Muster und KI-Vokabeln raus
2. **Variieren:** Satzrhythmus auflockern
3. **Einspritzen:** Minimale Personality-Elemente einfügen

Er fügt keinen besonderen Stil hinzu. Kein Lesch, kein Locker, kein Akademisch. Einfach: menschlich.

---

## Umschreib-Regeln (in dieser Reihenfolge anwenden)

### Schritt 1: Verbotene Phrasen entfernen
- Alle Phrasen aus der Verbotenen-Phrasen-Liste (`vokabeln.md`) streichen
- Ersetzen durch direkte Aussagen
- Wenn nach dem Streichen der Satz keinen Inhalt mehr hat: ganzen Satz streichen

### Schritt 2: Tier-1-Wörter ersetzen
- Jedes Tier-1-Wort durch den vorgeschlagenen Ersatz ersetzen
- Kontext beachten: "robust" in einer Server-Beschreibung kann bleiben, "robust" für eine Idee muss raus

### Schritt 3: Tier-2-Dichte prüfen
- Mehr als 1x pro 500 Wörter? Überschuss ersetzen
- Bevorzugt die einfachere Variante wählen

### Schritt 4: KI-Muster auflösen
- Jedes erkannte Muster (aus `ki-muster.md`) umschreiben
- Priorität: HOCH-Muster zuerst
- Die Nachher-Beispiele aus der Muster-Datei als Orientierung nutzen

### Schritt 5: Passiv → Aktiv
- Jede Passiv-Konstruktion prüfen: Gibt es ein konkretes Subjekt?
- "Es wird davon ausgegangen" → "Wir denken" / "Ich denke" / "Die Autoren gehen davon aus"
- "Die Konfiguration wird erstellt" → "Du erstellst die Konfiguration"

### Schritt 6: Satzrhythmus variieren
- Prüfe: Gibt es 3+ Sätze gleicher Länge hintereinander?
- Wenn ja: Einen Satz kürzen (Fragment?), einen verlängern (Nebensatz?)
- Ziel: Welle aus kurz-mittel-lang-kurz

### Schritt 7: Personality-Minimum
- Füge 1–2 Einschübe in Klammern ein (Technik 1)
- Prüfe ob mindestens 1 Satzfragment vorkommt
- Prüfe ob mindestens 1 Kontraktion möglich ist (gibt's, hat's, geht's)

### Schritt 8: Schluss prüfen
- Endet der Text mit einer generischen Schlussfolgerung? → Umschreiben oder streichen
- Gute Schlüsse: Konkrete nächste Aktion, offene Frage, ehrliche Einschätzung
- Schlechte Schlüsse: "Es bleibt spannend", "Die Zukunft sieht rosig aus"

---

## Tonalität des Basis-Layers

| Eigenschaft | Einstellung |
|-------------|------------|
| Formalität | Mittel (weder Behördendeutsch noch SMS) |
| Du/Sie | Beibehalten wie im Original |
| Fachbegriffe | Beibehalten, aber erklären wenn nötig |
| Humor | Nicht aktiv einbauen, aber nicht entfernen wenn vorhanden |
| Persönliche Meinung | Nicht einbauen (das macht der Autor) |
| Metaphern | Vorhandene verbessern, keine neuen hinzufügen |

---

## Vorher/Nachher-Beispiel (komplett)

### Vorher (KI-generiert):

> "Es ist wichtig zu beachten, dass OpenClaw eine grundlegend andere Herangehensweise an KI-Routing darstellt. Das System fungiert als nahtloser Vermittler zwischen verschiedenen KI-Modellen und ermöglicht es Benutzern, die robuste und skalierbare Architektur zu nutzen. Darüber hinaus bietet die Plattform eine ganzheitliche Lösung, die nicht nur die technische Implementierung umfasst, sondern auch die facettenreiche Landschaft der KI-Interaktion berücksichtigt. Studien zeigen, dass dieser Ansatz die Produktivität maßgeblich steigert. Die Zukunft sieht vielversprechend aus."

**Probleme:**
- 6 Tier-1-Wörter (grundlegend, nahtlos, robust, skalierbar, ganzheitlich, facettenreich)
- 3 verbotene Phrasen (Es ist wichtig zu beachten, nicht nur...sondern auch, Darüber hinaus)
- 3 KI-Muster (Werbesprache, Copula-Vermeidung, Generische Schlussfolgerung)
- Kein Rhythmus (alle Sätze 15–25 Wörter)
- Passiv + vage Zuschreibung

### Nachher (Basis-Layer):

> "OpenClaw routet KI-Anfragen anders als andere Systeme. Es sitzt zwischen den Modellen – Claude hier, GPT dort – und entscheidet, wer die Anfrage bekommt. Das spart Zeit. Die Architektur wächst mit deinen Anforderungen (ich hab sie mit 50 gleichzeitigen Anfragen getestet, kein Problem). Ob das die Produktivität steigert? Kommt drauf an was du vorher gemacht hast. Aber schneller geht's auf jeden Fall."

**Was sich geändert hat:**
- Alle Tier-1-Wörter ersetzt
- Alle verbotenen Phrasen entfernt
- Aktiv statt Passiv
- Satzrhythmus variiert (5, 16, 3, 17, 9, 10 Wörter)
- Ein Einschub in Klammern
- Eine Kontraktion (geht's)
- Konkrete Aussage statt generischem Schluss

---

## Grenzen des Basis-Layers

1. **Kein Stil-Hinzufügen:** Der Basis-Layer macht den Text nicht "besser" oder "interessanter". Er macht ihn nur weniger KI-haft.
2. **Keine Inhaltsänderung:** Fakten, Argumente und Struktur bleiben wie im Original.
3. **Keine Tonänderung:** Wenn das Original formal ist, bleibt es formal. Nur die KI-Signale werden entfernt.
4. **Kein Umstrukturieren:** Die Absatz- und Kapitelstruktur bleibt erhalten.

Für mehr Stil: Verwende einen spezifischen Stil-Layer (z.B. `lesch.md`).
