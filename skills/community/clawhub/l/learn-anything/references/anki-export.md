# Anki Flashcard Export Format

Generated flashcards can be imported directly into Anki.

## Format (CSV)

```csv
#Front,Back,Tags
What is spaced repetition?,Review material at increasing intervals to combat forgetting curve,"learning,psychology"
What does "po" indicate in Tagalog?,Respect marker used when speaking to elders,"tagalog,language"
What's the difference between tayo and kami?,"Tayo = we (inclusive, includes listener), Kami = we (exclusive, excludes listener)","tagalog,grammar"
```

## Anki Import Steps

1. Generate flashcards: `python generate-quiz.py [topic] --format anki`
2. Open Anki → File → Import
3. Select CSV file
4. Map fields: Field 1 = Front, Field 2 = Back, Field 3 = Tags
5. Import

## Cloze Deletion Format

For fill-in-the-blank style:

```
{{c1::Spaced repetition}} is the technique of reviewing material at {{c2::increasing intervals}}.
```

Import as "Cloze" note type in Anki.
