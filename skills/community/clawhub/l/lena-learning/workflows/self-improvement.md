<workflow>
<name>session-summary</name>
<description>Am Ende jeder Session - Learnings speichern</description>

<steps>
<step>Scanne die letzten Nachrichten nach Feedback</step>
<step>Extrahiere Korrekturen ("Nein, das ist falsch...", "Besser...")</step>
<step>Identifiziere neue Präferenzen</step>
<step>Schreibe in memory/YYYY-MM-DD.md</step>
<step>Update MEMORY.md wenn wichtig</step>
</steps>

<output>
Session-Summary mit Learnings, Korrekturen, neuen Präferenzen
</output>
</workflow>

<workflow>
<name>correction-handler</name>
<description>Wenn Thomas mich korrigiert - sofort speichern</description>

<steps>
<step>Erkenne Korrektur-Pattern</step>
<step>Speichere in memory/YYYY-MM-DD.md mit Zeitstempel</step>
<step>Prüfe ob Regel/Präferenz betroffen</step>
<step>Update AGENTS.md oder TOOLS.md wenn nötig</step>
<step>Bestätige Verbesserung</step>
</steps>

<output>
Korrektur dokumentiert + zukünftige Verbesserung
</output>
</workflow>

<workflow>
<name>preference-tracker</name>
<description>Thomas' Präferenzen im Auge behalten</description>

<steps>
<step>Check regelmäßig USER.md</step>
<note>Thomas' Präferenzen:
- Deutsch
- Autonom arbeiten
- Short-term & aggressiv
- Signals nur im Kanal, nicht DM
</note>
<step>Merke neue Patterns (kommunikation, timing, style)</step>
<step>Update bei Änderungen</step>
</steps>

<output>
Aktuelle Präferenzen-Übersicht
</output>
</workflow>