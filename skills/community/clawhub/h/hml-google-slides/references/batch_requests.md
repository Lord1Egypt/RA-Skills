# Google Slides Batch Request Patterns

Reference for `scripts/slides.py batch <presentationId> requests.json`

Full API docs: https://developers.google.com/slides/api/reference/rest/v1/presentations/batchUpdate

## Create a Slide

```json
[{
  "createSlide": {
    "objectId": "slide_001",
    "insertionIndex": 1,
    "slideLayoutReference": { "predefinedLayout": "TITLE_AND_BODY" },
    "placeholderIdMappings": [
      { "layoutPlaceholder": { "type": "TITLE" }, "objectId": "title_001" },
      { "layoutPlaceholder": { "type": "BODY" }, "objectId": "body_001" }
    ]
  }
}]
```

Predefined layouts: `BLANK`, `CAPTION_ONLY`, `TITLE`, `TITLE_AND_BODY`, `TITLE_AND_TWO_COLUMNS`, `TITLE_ONLY`, `SECTION_HEADER`, `SECTION_TITLE_AND_DESCRIPTION`, `ONE_COLUMN_TEXT`, `MAIN_POINT`, `BIG_NUMBER`

## Insert Text

```json
[{
  "insertText": {
    "objectId": "title_001",
    "text": "My Slide Title"
  }
}]
```

## Delete Text

```json
[{
  "deleteText": {
    "objectId": "body_001",
    "textRange": { "type": "ALL" }
  }
}]
```

## Format Text (Bold, Color, Font Size)

```json
[{
  "updateTextStyle": {
    "objectId": "title_001",
    "style": {
      "bold": true,
      "fontSize": { "magnitude": 36, "unit": "PT" },
      "foregroundColor": {
        "opaqueColor": { "rgbColor": { "red": 0.2, "green": 0.2, "blue": 0.8 } }
      }
    },
    "textRange": { "type": "ALL" },
    "fields": "bold,fontSize,foregroundColor"
  }
}]
```

## Insert Image

```json
[{
  "createImage": {
    "objectId": "img_001",
    "url": "https://example.com/image.png",
    "elementProperties": {
      "pageObjectId": "slide_001",
      "size": {
        "height": { "magnitude": 3000000, "unit": "EMU" },
        "width":  { "magnitude": 4000000, "unit": "EMU" }
      },
      "transform": {
        "scaleX": 1, "scaleY": 1,
        "translateX": 1000000, "translateY": 1000000,
        "unit": "EMU"
      }
    }
  }
}]
```

Note: 1 inch = 914400 EMU. Slide is typically 9144000 × 5143500 EMU (10" × 7.5" at 72 DPI... actually 9144000/914400 = 10", 5143500/914400 = 5.625")

## Set Slide Background Color

```json
[{
  "updatePageProperties": {
    "objectId": "slide_001",
    "pageProperties": {
      "pageBackgroundFill": {
        "solidFill": {
          "color": {
            "rgbColor": { "red": 0.1, "green": 0.1, "blue": 0.1 }
          }
        }
      }
    },
    "fields": "pageBackgroundFill"
  }
}]
```

## Move / Resize an Element

```json
[{
  "updatePageElementTransform": {
    "objectId": "img_001",
    "transform": {
      "scaleX": 1, "scaleY": 1,
      "translateX": 2000000, "translateY": 1500000,
      "unit": "EMU"
    },
    "applyMode": "ABSOLUTE"
  }
}]
```

## Delete an Element

```json
[{
  "deleteObject": {
    "objectId": "img_001"
  }
}]
```

## Duplicate a Slide

```json
[{
  "duplicateObject": {
    "objectId": "slide_001"
  }
}]
```

## Replace All Text (find & replace across whole deck)

```json
[{
  "replaceAllText": {
    "containsText": { "text": "{{COMPANY}}", "matchCase": false },
    "replaceText": "Acme Corp"
  }
}]
```

## Common EMU Conversions

| Inches | EMU       |
|--------|-----------|
| 1"     | 914400    |
| 2"     | 1828800   |
| 3"     | 2743200   |
| 5"     | 4572000   |
| 10"    | 9144000   |

Standard slide size: 9144000 × 5143500 EMU (widescreen 16:9)
