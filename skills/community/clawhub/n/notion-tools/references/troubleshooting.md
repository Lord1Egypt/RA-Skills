# Troubleshooting

Use these checks before assuming the payload is wrong:

- `401 unauthorized`
  Check that `NOTION_KEY` is set correctly and the token file contains only the secret.
- `403 restricted_resource`
  The integration usually is not shared to the target page or database.
- `404 object_not_found`
  The ID may be wrong, or the integration cannot access the object.
- Validation errors on properties
  Read the current page or data source schema again and match exact property names and types.
- Query returns nothing
  Confirm you are using the `data_source_id` for queries and not only the database parent ID.
