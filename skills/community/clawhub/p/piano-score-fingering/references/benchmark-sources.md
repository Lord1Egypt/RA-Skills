# Benchmark Sources and Measurement Scope

No third-party scores or reference fingering datasets are distributed. Prefer locally held, fingered, single-piece PDFs with a declared level-5-or-below assessment. Public sources supplement generalization diagnostics.

## Sources

- Standard scales: Piano.org Major Scale Fingering Chart. The regression uses 12 distinct major keys. https://piano.org/theory/piano-fingering/
- Mutopia Hanon Part I: digital PDF/MIDI/LilyPond, CC BY-SA 4.0, with fingers. Useful for technical/anchor/repeat tests, not real-piece acceptance. https://www.mutopiaproject.org/cgibin/piece-info.cgi?id=2037
- Piano Protege Curriculum: CC BY-SA 4.0 MIDI/finger labels; symbolic solver tests only, no aligned original PDF geometry. https://huggingface.co/datasets/riyaranjan/piano-protege-curriculum
- MuseTrainer Library: Canon_in_D_easy, Greensleeves_for_Piano_easy_and_beautiful, Fur_Elise_fingered contain editorial anchors. Strip fingers at generation with --ignore-existing. Easy titles are not official grades. Other unmarked files supply structure/compliance tests only. https://github.com/musetrainer/library
- Bach/Schop beginner arrangement, Jesus Alegria dos Homens: three-page digital PDF with editorial fingers, as an independent supplemental visual diagnostic. Check its stated rights and keep it outside the package. https://commons.wikimedia.org/wiki/File:Bach_sheet_for_beginners_jesu_joy.pdf
- PIG requires legitimate user registration and license review. Do not mirror, redistribute, or mix its ungraded stress tests with level-5 metrics. Tool reference: https://github.com/JuliaMusic/PianoFingering.jl
- Gurlitt public single-piece digital editions: https://michaelkravchuk.com/free-piano-sheet-music-first-lessons-op-117-no-8-gurlitt/ and https://michaelkravchuk.com/free-piano-sheet-music-first-lessons-op-117-no-7-gurlitt/ . Respect the publisher's noncommercial-use terms; retain only local test artifacts.

## Public single-piece PDF candidates

Verify actual used pages, difficulty, rights, and visible fingers before inclusion.

- Minuet in G, BWV Anh.114: https://www.mutopiaproject.org/ftp/BachJS/BWVAnh114/anna-magdalena-04/anna-magdalena-04-a4.pdf
- Minuet in B-flat, BWV Anh.118: https://www.mutopiaproject.org/ftp/BachJS/BWVAnh118/BWV-118/BWV-118-a4.pdf
- Polonaise in G minor, BWV Anh.119: https://www.mutopiaproject.org/ftp/BachJS/BWVAnh119/BWV-119/BWV-119-a4.pdf
- Minuet in A minor, BWV Anh.120: https://www.mutopiaproject.org/ftp/BachJS/BWVAnh120/BWV-120/BWV-120-a4.pdf
- Musette, BWV Anh.126: https://www.mutopiaproject.org/ftp/BachJS/BWVAnh126/anna-magdalena-22/anna-magdalena-22-a4.pdf
- Clementi Op.36 No.1: https://www.mutopiaproject.org/ftp/ClementiM/O36/sonatina-1/sonatina-1-let.pdf
- Schumann Melodie Op.68 No.1: https://www.mutopiaproject.org/ftp/SchumannR/O68/schumann-op68-01-melodie/schumann-op68-01-melodie-a4.pdf
- Schumann Chanson fredonnee Op.68 No.3: https://www.mutopiaproject.org/ftp/SchumannR/O68/schumann-op68-03-chanson-fredonnee/schumann-op68-03-chanson-fredonnee-a4.pdf
- Schumann Petite piece Op.68 No.5: https://www.mutopiaproject.org/ftp/SchumannR/O68/schumann-op68-05-petite-piece/schumann-op68-05-petite-piece-a4.pdf
- Handel Sonatina HWV585: https://www.mutopiaproject.org/ftp/HandelGF/HWV585/sonatina-in-b-flat-major/sonatina-in-b-flat-major-a4.pdf
- Tchaikovsky Old French Song: https://www.mutopiaproject.org/ftp/TchaikovskyPI/O39/16OldFrenchSong/16OldFrenchSong-a4.pdf
- Satie Gymnopedie No.1, an estimated boundary case: https://www.mutopiaproject.org/ftp/SatieE/gymnopedie_1/gymnopedie_1-a4.pdf
- Burgmuller La Candeur, use only where standalone etudes are permitted: https://www.mutopiaproject.org/ftp/BurgmullerJFF/O100/25EF-01/25EF-01-a4.pdf
- Schumann First Sorrow, complex voice/tie stress sample rather than level-5 acceptance: https://www.mutopiaproject.org/ftp/SchumannR/O68/schumann-op68-16-premier-chagrin/schumann-op68-16-premier-chagrin-a4.pdf

Scans, photographs, and multi-exercise collections are excluded from the clean digital-PDF acceptance corpus. They may support separate diagnostics.

## Local private corpus

The maintainer holds Tears, Vivaldi Variation, Morning Grass, Water Lily, Lovely Home, Acacia Flower, and Before Spring Ends with partial editorial fingers, declared within level five by the provider. Keep PDFs/anchors private. Fingerprint inputs with create_private_benchmark_manifest.py and independently transcribe readable digits.

Partial PDF references do not require matching MusicXML. For structured references, compare only original locked fingers and validate stable pitch/hand identities.

```bash
python3 scripts/run_editorial_mxl_benchmark.py \
  --score canon=/path/Canon_in_D_easy.mxl \
  --score greensleeves=/path/Greensleeves_for_Piano_easy_and_beautiful.mxl \
  --score fur-elise=/path/Fur_Elise_fingered.mxl \
  --out-dir editorial-mxl-benchmark
```

Use --part-id piece-id=part-id only after confirming the piano part. Split hands require paired --rh-part-id and --lh-part-id. Do not infer RH from first-part order to increase sample count.

## Reporting and difficulty

Editorial accuracy is exact agreement with a specified edition, not a judgment that all alternatives are unplayable. Preserve hard-constraint and musical review separately. Keep per-hand/per-piece denominators, failed samples, fingerprints, audit reports, rendered pages, and independent holdouts. Discard unsupported historical headline percentages and rerun current manifests before making claims. Separate private and public results.

An engineering estimate of level five or below normally means no more than three simultaneous notes per hand, ordinary spans within an octave, no sustained fast leaps or complex independent polyphony, mostly half/quarter/eighth values with occasional sixteenths, and an appropriate beginner/intermediate tempo. File names such as easy do not certify a grade. State actual included measures and rationale; this definition does not replace any examination board.
