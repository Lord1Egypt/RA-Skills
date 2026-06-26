# python-docx API Summary

This document summarizes the core APIs of the `python-docx` library for quick reference.

## Document Object
- `Document()`: create a new document.
- `Document("file.docx")`: open an existing document.
- `save("file.docx")`: save the document.
- `add_heading(text, level)`: add a heading.
- `add_paragraph(text, style)`: add a paragraph.
- `add_picture(path, width, height)`: add an image.
- `add_table(rows, cols, style)`: add a table.
- `paragraphs`: list of paragraphs in the document.
- `tables`: list of tables in the document.
- `sections`: list of sections in the document.
- `styles`: collection of document styles.
- `core_properties`: document core properties such as author and title.

## Paragraph and Run Objects
- `paragraph.add_run(text, style)`: add a text run to a paragraph.
- `paragraph.alignment`: paragraph alignment.
- `paragraph.style`: paragraph style.
- `paragraph.text`: plain text content of the paragraph.
- `run.bold`: bold.
- `run.italic`: italic.
- `run.underline`: underline.
- `run.font.name`: font name.
- `run.font.size`: font size in points.
- `run.font.color.rgb`: font color.

## Table and Cell Objects
- `table.add_row()`: add a row.
- `table.cell(row_idx, col_idx)`: get a specific cell.
- `table.rows`: collection of table rows.
- `table.columns`: collection of table columns.
- `table.style`: table style.
- `cell.text`: text content of the cell.
- `cell.merge(other_cell)`: merge cells.
- `cell.vertical_alignment`: vertical alignment of the cell.

## Section Object
- `section.header` / `section.footer`: header and footer.
- `section.page_width` / `section.page_height`: page width and height.
- `section.left_margin` / `section.right_margin`: left and right margins.
- `section.orientation`: page orientation.

## Common Units and Enums
- `Inches()`, `Cm()`, `Pt()`: length units.
- `RGBColor()`: RGB color.
- `WD_PARAGRAPH_ALIGNMENT`: paragraph alignment enum.
- `WD_TABLE_ALIGNMENT`: table alignment enum.
- `WD_ORIENTATION`: page orientation enum.
