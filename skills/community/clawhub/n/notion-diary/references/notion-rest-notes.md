# Notion REST Notes

## Runtime assumptions

- The bundled script uses the Notion REST API, not Notion MCP.
- It expects `NOTION_API_KEY` in the process environment.
- It uses the current public API version `2026-03-11`.

## What the script manages

- Finds an existing diary database under a parent page, or creates one.
- Works with a single primary data source.
- Creates or updates pages for each date and mode.
- Uploads local files up to 20 MB using the direct upload flow when image paths are available.

## What the script does not manage

- A first-class calendar view. Create the calendar view once in the Notion UI and point it at the `Date` property.
- Workspace-wide search for arbitrary diary databases.
- Large multi-part uploads above 20 MB.

## Default schema

- `Title` title
- `Date` date
- `Mode` select: `Diary`, `Report`
- `Style` select: `纪实简洁`, `温柔叙事`, `克制反思`, `轻文艺`
- `Summary` rich text
- `Photos` files
