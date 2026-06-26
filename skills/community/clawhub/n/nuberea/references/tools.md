# NuBerea MCP Tools Reference

Auto-generated from the live MCP server. 57 tools.

### macula_hebrew_query_verse
Query Hebrew Bible (Masoretic Text) morphological data for a specific verse. Use standard book abbreviations (Gen, Exod, Lev, Ps, Isa, etc.)

- `book`: string (required) — Book name or abbreviation (e.g., "Gen")
- `chapter`: number (required) — Chapter number
- `verse`: number (required) — Verse number

### macula_hebrew_search_lemma
Search for occurrences of a lemma (dictionary form) across the Hebrew Bible (Masoretic Text).

- `lemma`: string (required) — Lemma to search for in Hebrew
- `limit`: number — Maximum results to return

### macula_hebrew_search_strong
Search for occurrences by Strong's number in the Hebrew Bible (Masoretic Text).

- `strong`: string (required) — Strong's number (e.g., "1234")
- `limit`: number — Maximum results to return

### macula_hebrew_search_word
Search for occurrences of a word (surface form) in the Hebrew Bible (Masoretic Text).

- `word`: string (required) — Word text to search for
- `limit`: number — Maximum results to return

### macula_hebrew_get_word_by_ref
Get complete morphological data for a single word by its unique reference in the Hebrew Bible (Masoretic Text).

- `ref`: string (required) — Word reference in format "BOOK C:V!W"

### macula_hebrew_run_sql
Execute a custom SQL query against the Hebrew Bible (Masoretic Text) database. Read-only queries only.

- `sql`: string (required) — SQL query to execute (SELECT only)

### macula_greek_query_verse
Query Greek New Testament morphological data for a specific verse. Use standard book abbreviations (Matt, Mark, Luke, John, Acts, Rom, Rev, etc.)

- `book`: string (required) — Book name or abbreviation (e.g., "Matt")
- `chapter`: number (required) — Chapter number
- `verse`: number (required) — Verse number

### macula_greek_search_lemma
Search for occurrences of a lemma (dictionary form) across the Greek New Testament.

- `lemma`: string (required) — Lemma to search for in Greek
- `limit`: number — Maximum results to return

### macula_greek_search_strong
Search for occurrences by Strong's number in the Greek New Testament.

- `strong`: string (required) — Strong's number (e.g., "1234")
- `limit`: number — Maximum results to return

### macula_greek_search_word
Search for occurrences of a word (surface form) in the Greek New Testament.

- `word`: string (required) — Word text to search for
- `limit`: number — Maximum results to return

### macula_greek_get_word_by_ref
Get complete morphological data for a single word by its unique reference in the Greek New Testament.

- `ref`: string (required) — Word reference in format "BOOK C:V!W"

### macula_greek_run_sql
Execute a custom SQL query against the Greek New Testament database. Read-only queries only.

- `sql`: string (required) — SQL query to execute (SELECT only)

### macula_lxx_query_verse
Query Septuagint (LXX) morphological data for a specific verse. Use standard book abbreviations (Gen, Exod, Ps, Isa, Dan, etc.)

- `book`: string (required) — Book name or abbreviation (e.g., "Gen")
- `chapter`: number (required) — Chapter number
- `verse`: number (required) — Verse number

### macula_lxx_search_lemma
Search for occurrences of a lemma (dictionary form) across the Septuagint (LXX).

- `lemma`: string (required) — Lemma to search for in Greek
- `limit`: number — Maximum results to return

### macula_lxx_search_strong
Search for occurrences by Strong's number in the Septuagint (LXX).

- `strong`: string (required) — Strong's number (e.g., "1234")
- `limit`: number — Maximum results to return

### macula_lxx_search_word
Search for occurrences of a word (surface form) in the Septuagint (LXX).

- `word`: string (required) — Word text to search for
- `limit`: number — Maximum results to return

### macula_lxx_get_word_by_ref
Get complete morphological data for a single word by its unique reference in the Septuagint (LXX).

- `ref`: string (required) — Word reference in format "BOOK C:V!W"

### macula_lxx_run_sql
Execute a custom SQL query against the Septuagint (LXX) database. Read-only queries only.

- `sql`: string (required) — SQL query to execute (SELECT only)

### lexicon_lsj_lookup
Look up a word in the Liddell-Scott-Jones Greek Lexicon. Returns the full dictionary entry.

- `term`: string (required) — Greek word to look up (e.g., "λόγος")

### lexicon_lsj_search
Search for entries matching a pattern in the Liddell-Scott-Jones Greek Lexicon. Wildcards added automatically — do NOT include %.

- `pattern`: string (required) — Greek text to search for (wildcards added automatically)
- `limit`: number — Maximum results to return

### lexicon_lsj_search_definition
Search Liddell-Scott-Jones Greek Lexicon by definition text (find words defined with specific English terms).

- `text`: string (required) — Text to search for in definitions
- `limit`: number — Maximum results to return

### lexicon_lsj_run_sql
Execute a custom SQL query against the Liddell-Scott-Jones Greek Lexicon database. Table: entries. Fields: id, headword, definition_text, morph_forms, greek_forms, latin_forms. Use CAST(COUNT(*) AS INTEGER) for aggregates.

- `sql`: string (required) — SQL query to execute (SELECT only)

### lexicon_lsj_search_latin
Search Liddell-Scott-Jones Greek Lexicon using Latin transliteration (e.g., "logos" finds λόγος).

- `form`: string (required) — Latin/English transliteration of Greek word
- `limit`: number — Maximum results to return

### lexicon_lsj_search_strong
Look up a word by Strong's number in the Liddell-Scott-Jones Greek Lexicon. For Hebrew: "1" for H1, "430" for H430. For Greek: "25" or "G25".

- `strong`: string (required) — Strong's number without prefix (e.g., "1", "430")

### lexicon_bdb_lookup
Look up a word in the BDB Hebrew Lexicon. Returns the full dictionary entry.

- `term`: string (required) — Hebrew/Aramaic word to look up (e.g., "אָב")

### lexicon_bdb_search
Search for entries matching a pattern in the BDB Hebrew Lexicon. Wildcards added automatically — do NOT include %.

- `pattern`: string (required) — Hebrew/Aramaic text to search for (wildcards added automatically)
- `limit`: number — Maximum results to return

### lexicon_bdb_search_definition
Search BDB Hebrew Lexicon by definition text (find words defined with specific English terms).

- `text`: string (required) — Text to search for in definitions
- `limit`: number — Maximum results to return

### lexicon_bdb_run_sql
Execute a custom SQL query against the BDB Hebrew Lexicon database. Table: entries. Fields: id, strong, strong_id, bdb_id, hebrew, transliteration, pos, short_def, language, pronunciation, strong_meaning, usage, bdb_text, bdb_refs, bdb_senses, bdb_stems, bdb_defs, bdb_pos, twot, etymology_type, etymology_root, augmented_strongs. Use CAST(COUNT(*) AS INTEGER) for aggregates.

- `sql`: string (required) — SQL query to execute (SELECT only)

### lexicon_bdb_search_strong
Look up a word by Strong's number in the BDB Hebrew Lexicon. For Hebrew: "1" for H1, "430" for H430. For Greek: "25" or "G25".

- `strong`: string (required) — Strong's number without prefix (e.g., "1", "430")

### lexicon_bdb_search_transliteration
Search BDB Hebrew Lexicon by transliteration. Plain ASCII works — diacritics stripped automatically (e.g., "adam" finds אָדָם).

- `form`: string (required) — Transliterated form — plain ASCII works (e.g., "ab", "adam", "dabar")
- `limit`: number — Maximum results to return

### lexicon_bdb_search_pos
Search BDB Hebrew Lexicon by part of speech (V=Verb, N=Noun, Np=Proper Name, A=Adjective, etc.).

- `pos`: string (required) — Part of speech code (e.g., "V", "N", "Np")
- `limit`: number — Maximum results to return

### lexicon_abbott_smith_lookup
Look up a word in the Abbott-Smith Manual Greek Lexicon. Returns the full dictionary entry.

- `term`: string (required) — Greek word to look up (e.g., "ἀγαπάω")

### lexicon_abbott_smith_search
Search for entries matching a pattern in the Abbott-Smith Manual Greek Lexicon. Wildcards added automatically — do NOT include %.

- `pattern`: string (required) — Greek text to search for (wildcards added automatically)
- `limit`: number — Maximum results to return

### lexicon_abbott_smith_search_definition
Search Abbott-Smith Manual Greek Lexicon by definition text (find words defined with specific English terms).

- `text`: string (required) — Text to search for in definitions
- `limit`: number — Maximum results to return

### lexicon_abbott_smith_run_sql
Execute a custom SQL query against the Abbott-Smith Manual Greek Lexicon database. Table: entries. Fields: entry_id, lemma, strong, pos, occurrences_nt, gloss, definition, form_text, scripture_refs, cross_refs. Use CAST(COUNT(*) AS INTEGER) for aggregates.

- `sql`: string (required) — SQL query to execute (SELECT only)

### lexicon_abbott_smith_search_strong
Look up a word by Strong's number in the Abbott-Smith Manual Greek Lexicon. For Hebrew: "1" for H1, "430" for H430. For Greek: "25" or "G25".

- `strong`: string (required) — Strong's number without prefix (e.g., "1", "430")

### bible_kjv_get_verse
Look up a specific verse from the King James Version (Cambridge Paragraph Bible).

- `book`: string (required) — Book abbreviation (e.g., "Gen")
- `chapter`: number (required) — Chapter number
- `verse`: number (required) — Verse number

### bible_kjv_get_chapter
Read an entire chapter from the King James Version (Cambridge Paragraph Bible).

- `book`: string (required) — Book abbreviation (e.g., "Gen")
- `chapter`: number (required) — Chapter number

### bible_kjv_get_verse_range
Read a range of verses within a chapter from the King James Version (Cambridge Paragraph Bible).

- `book`: string (required) — Book abbreviation (e.g., "Gen")
- `chapter`: number (required) — Chapter number
- `startVerse`: number (required) — Starting verse number
- `endVerse`: number (required) — Ending verse number

### bible_kjv_search_text
Search for verses containing specific text in the King James Version (Cambridge Paragraph Bible).

- `query`: string (required) — Text to search for (case-insensitive)
- `limit`: number — Maximum results to return

### bible_kjv_list_books
List all books in the King James Version (Cambridge Paragraph Bible) with chapter counts.

### bible_kjv_run_sql
Execute a custom SQL query against the King James Version (Cambridge Paragraph Bible) database. Read-only queries only.

- `sql`: string (required) — SQL query to execute (SELECT only)

### transcription_cntr_get_verse
Get manuscript transcriptions for a verse from CNTR Greek NT Transcriptions

- `book`: string (required) — Book abbreviation (e.g., "Matt", "John")
- `chapter`: number (required) — Chapter number
- `verse`: number (required) — Verse number

### transcription_cntr_list_manuscripts
List manuscripts in CNTR Greek NT Transcriptions

### transcription_cntr_search_text
Search text in CNTR Greek NT Transcriptions

- `query`: string (required) — Greek text to search for
- `limit`: number — Maximum results to return (default: 50)

### transcription_cntr_run_sql
Run SQL on CNTR Greek NT Transcriptions

- `sql`: string (required) — SQL SELECT query to execute against the "transcriptions" table

### scroll_dss_get_scroll
Get word-level annotations from a scroll in Dead Sea Scrolls

- `scroll`: string (required) — Scroll identifier (e.g., "1QS", "1QpHab")
- `limit`: number — Maximum words to return (default: 500)

### scroll_dss_get_fragment
Get word-level annotations from a scroll fragment in Dead Sea Scrolls

- `scroll`: string (required) — Scroll identifier
- `fragment`: string (required) — Fragment identifier

### scroll_dss_get_line
Get word-level annotations from a scroll fragment line in Dead Sea Scrolls

- `scroll`: string (required) — Scroll identifier
- `fragment`: string (required) — Fragment identifier
- `line`: string (required) — Line identifier

### scroll_dss_list_scrolls
List all scrolls in Dead Sea Scrolls

### scroll_dss_search_lemma
Search by lemma in Dead Sea Scrolls

- `lemma`: string (required) — Hebrew/Aramaic lemma (e.g., "אֱלֹהִים")
- `limit`: number — Maximum results to return (default: 50)

### scroll_dss_search_text
Search text in Dead Sea Scrolls

- `query`: string (required) — Hebrew/Aramaic text to search for
- `limit`: number — Maximum results to return (default: 50)

### scroll_dss_run_sql
Run SQL on Dead Sea Scrolls

- `sql`: string (required) — SQL SELECT query to execute against the "scrolls" table

### synoptic_find_parallels
Find synoptic gospel parallels for a single verse. For verse ranges, use synoptic_find_parallels_range.

- `book`: string (required) — Book name (e.g., "Matt", "Mark", "Luke", "John")
- `chapter`: number (required) — Chapter number
- `verse`: number (required) — Verse number

### synoptic_find_parallels_range
Find synoptic gospel parallels for a verse range within a single chapter. Limited to 50 verses per lookup.

- `book`: string (required) — Book name (e.g., "Matt", "Mark", "Luke", "John")
- `chapter`: number (required) — Chapter number
- `startVerse`: number (required) — First verse of the range
- `endVerse`: number — Last verse of the range (defaults to startVerse)

### synoptic_search
Search synoptic gospel parallels by topic, title, or keyword.

- `query`: string (required) — Search term to match against pericope titles
- `limit`: number — Maximum results to return

### synoptic_list_pericopes
List synoptic gospel pericopes from the Aland Synopsis (330 pericopes). Optionally filter to synoptic parallels only or to a specific gospel.

- `synopticOnly`: boolean — If true, only show synoptic parallels
- `book`: string — Filter to pericopes present in a specific gospel (e.g., "Matt", "Mark", "Luke", "John")
- `limit`: number — Maximum results to return

