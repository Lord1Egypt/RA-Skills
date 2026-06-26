# Docs, Slides, and Forms Reference

## Docs

```bash
# Create
DOC_ID=$(gws docs documents create --json '{"title":"My Doc"}' --params '{}' 2>/dev/null | tail -n +2 | jq -r '.documentId')

# Extract plain text
gws docs documents get --params '{"documentId":"ID"}' 2>/dev/null | tail -n +2 | jq '[.body.content[]|select(.paragraph)|.paragraph.elements[]?|select(.textRun)|.textRun.content]|join("")'

# Insert text (index 1 = start)
gws docs documents batchUpdate --json '{"requests":[{"insertText":{"location":{"index":1},"text":"Hello\n"}}]}' --params '{"documentId":"ID"}'

# Bold
gws docs documents batchUpdate --json '{"requests":[{"updateTextStyle":{"range":{"startIndex":1,"endIndex":6},"textStyle":{"bold":true},"fields":"bold"}}]}' --params '{"documentId":"ID"}'

# Heading
gws docs documents batchUpdate --json '{"requests":[{"updateParagraphStyle":{"range":{"startIndex":1,"endIndex":10},"style":{"namedStyleType":"HEADING_1"},"fields":"namedStyleType"}}]}' --params '{"documentId":"ID"}'

# Insert image
gws docs documents batchUpdate --json '{"requests":[{"insertInlineImage":{"uri":"https://example.com/img.png","location":{"index":1}}}]}' --params '{"documentId":"ID"}'

# Bullet list
gws docs documents batchUpdate --json '{"requests":[{"createParagraphBullets":{"range":{"startIndex":1,"endIndex":20},"bulletPreset":"BULLET_DISC_CIRCLE_SQUARE"}}]}' --params '{"documentId":"ID"}'
```

## Slides

Coordinates use EMU units (1 inch = 914400 EMU).

```bash
SLIDE_ID=$(gws slides presentations create --json '{"title":"My Slides"}' --params '{}' 2>/dev/null | tail -n +2 | jq -r '.presentationId')

# Create text box with text
gws slides presentations batchUpdate --json '{"requests":[{"createShape":{"objectId":"s1","shapeType":"TEXT_BOX","elementProperties":{"pageObjectId":"p1","size":{"width":{"magnitude":4000000,"unit":"EMU"},"height":{"magnitude":300000,"unit":"EMU"}},"transform":{"scaleX":1,"scaleY":1,"translateX":100000,"translateY":100000,"unit":"EMU"}}}},{"insertText":{"objectId":"s1","text":"Hello!"}}]}' --params '{"presentationId":"ID"}'

# New slide
gws slides presentations batchUpdate --json '{"requests":[{"createSlide":{"objectId":"slide2"}}]}' --params '{"presentationId":"ID"}'

# Insert image
gws slides presentations batchUpdate --json '{"requests":[{"createImage":{"url":"https://example.com/img.png","elementProperties":{"pageObjectId":"p1","size":{"width":{"magnitude":3000000,"unit":"EMU"},"height":{"magnitude":2000000,"unit":"EMU"}},"transform":{"scaleX":1,"scaleY":1,"translateX":500000,"translateY":500000,"unit":"EMU"}}}}]}' --params '{"presentationId":"ID"}'
```

## Forms

`forms create` only accepts `title`. Add questions via `batchUpdate`.

```bash
FORM_ID=$(gws forms forms create --json '{"info":{"title":"Survey"}}' --params '{}' 2>/dev/null | tail -n +2 | jq -r '.formId')
```

### Question types

```bash
# Text (short/paragraph)
gws forms forms batchUpdate --json '{"requests":[{"createItem":{"location":{"index":0},"item":{"title":"Your name?","questionItem":{"question":{"required":true,"textQuestion":{}}}}}}]}' --params '{"formId":"ID"}'

# Radio (single choice)
gws forms forms batchUpdate --json '{"requests":[{"createItem":{"location":{"index":1},"item":{"title":"Pick one","questionItem":{"question":{"required":true,"choiceQuestion":{"type":"RADIO","options":[{"value":"A"},{"value":"B"},{"value":"C"}]}}}}}}]}' --params '{"formId":"ID"}'

# Checkbox (multi-select)
gws forms forms batchUpdate --json '{"requests":[{"createItem":{"location":{"index":2},"item":{"title":"Select all","questionItem":{"question":{"required":true,"choiceQuestion":{"type":"CHECKBOX","options":[{"value":"X"},{"value":"Y"}]}}}}}}]}' --params '{"formId":"ID"}'

# Dropdown
gws forms forms batchUpdate --json '{"requests":[{"createItem":{"location":{"index":3},"item":{"title":"Choose","questionItem":{"question":{"required":true,"choiceQuestion":{"type":"DROP_DOWN","options":[{"value":"1"},{"value":"2"}]}}}}}}]}' --params '{"formId":"ID"}'

# Date / Time
gws forms forms batchUpdate --json '{"requests":[{"createItem":{"location":{"index":4},"item":{"title":"Date?","questionItem":{"question":{"required":false,"dateQuestion":{"type":"DATE"}}}}}}]}' --params '{"formId":"ID"}'

# Scale (1-5 / 1-10)
gws forms forms batchUpdate --json '{"requests":[{"createItem":{"location":{"index":5},"item":{"title":"Rate","questionItem":{"question":{"required":true,"scaleQuestion":{"low":1,"high":5}}}}}}]}' --params '{"formId":"ID"}'
```

### Read responses

```bash
gws forms forms responses list --params '{"formId":"ID"}'
```
