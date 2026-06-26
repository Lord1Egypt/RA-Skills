# LiteParse Output Examples

## Text Format (default)

```
$ lit parse document.pdf

Page 1
-------
This is the extracted text from page one.
Tables and columns may appear inline with spacing preserved.

Page 2
-------
Continued content here...
```

## JSON Format

```json
{
  "pages": [
    {
      "pageNumber": 1,
      "width": 612,
      "height": 792,
      "text": "Full page text content...",
      "items": [
        {
          "text": "Section Heading",
          "bbox": [72, 720, 300, 740],
          "fontSize": 14,
          "fontFamily": "Helvetica-Bold"
        },
        {
          "text": "Body paragraph text here.",
          "bbox": [72, 680, 540, 695],
          "fontSize": 10,
          "fontFamily": "Helvetica"
        }
      ]
    }
  ],
  "metadata": {
    "totalPages": 2,
    "title": "Document Title",
    "author": "Author Name"
  }
}
```

## Bbox Format

`bbox` arrays are `[x1, y1, x2, y2]` in PDF coordinate space (origin bottom-left, units in points at 72 DPI).

Convert to pixel position at custom DPI:
```
pixel_x = (x1 / 72) * dpi
pixel_y = (page_height_pts - y2) / 72 * dpi
```

## Batch Parse Output

Each input file produces a corresponding output file in the output directory:
```
input/
  report.pdf     → output/report.txt (or .json)
  memo.docx      → output/memo.txt
  data.xlsx      → output/data.txt
```

## Screenshot Output

```
./screenshots/
  page-1.png
  page-2.png
  page-3.png
```

Default DPI is 150 (good for most text). Use 300 for dense or small-text documents fed to vision models.
