# Writes, concurrency, and relationships

## Before every mutation

Confirm `InsertRestrictions`, `UpdateRestrictions`, `DeleteRestrictions`, navigation restrictions, required/non-updatable properties, permissions, and business prerequisites. Resolve the exact resource and current ETag. A precise user request authorizes that operation; metadata inspection or a request to “check” data does not.

Use `Content-Type: application/json` and an appropriate `OData-Version`. Ask for `Prefer: return=representation` when the resulting entity is useful, or `return=minimal` when supported and sufficient.

## Create

```http
POST {service-root}/Products
Content-Type: application/json

{"Name":"Road Bike","Price":1200}
```

Send declared writable properties with correctly typed JSON values. A successful create commonly returns `201 Created`, a representation or empty body, and `Location`, `OData-EntityId`, and/or `ETag`. Do not retry an ambiguous create unless an idempotency mechanism or a unique-key read proves it did not commit.

Deep insert can create related new entities inline when advertised/supported. Do not confuse nested entities with bindings to existing entities.

## Update, replace, and upsert

- PATCH applies a partial update; omitted properties remain unchanged.
- PUT replaces an entity; omitted properties may reset to defaults or null according to the model.
- PATCH/PUT to a missing entity may be treated as upsert unless the service or request conditions prevent it.

Prefer:

```http
PATCH {edit-url}
If-Match: W/"current-etag"
Content-Type: application/json

{"Price":1250}
```

Use the ETag returned for that resource. `412 Precondition Failed` means state changed; re-read and reconcile instead of overwriting. `428 Precondition Required` means an ETag condition is required. `If-Match: *` deliberately ignores version identity and needs explicit acceptance of that risk.

Do not send computed, server-generated, immutable, undeclared, or read-restricted values back reflexively. A GET representation is not automatically a valid update payload.

## Delete

DELETE the entity's edit URL with its ETag when available. The body should be empty. Successful deletion normally returns `204 No Content`. Read-before-delete and verify key identity, especially when natural-language names are non-unique.

## Relationship links

Use navigation `/$ref` to relate existing entities without recreating them. The reference body identifies the target:

```json
{"@odata.id":"https://example.test/odata/Products(7)"}
```

- Add to a collection navigation property: POST `Orders(1)/Items/$ref`.
- Set a single-valued navigation property: PUT `Orders(1)/Customer/$ref`.
- Remove a single-valued link: DELETE `Orders(1)/Customer/$ref`.
- Remove one collection link: DELETE the collection reference URL using the service-supported v4 form, commonly `Orders(1)/Items/$ref?$id={encoded-target-id}`; confirm metadata/provider behavior.

Deleting a link is different from deleting the related entity. For containment, deleting the contained resource can have lifecycle effects; inspect containment and cascade rules first.
