# Service discovery and capabilities

Use this reference when the entity model, service version, or supported query features are unknown.

## Identify the service root

The service root is the stable URL before entity-set and OData system segments. Preserve provider-specific path prefixes and trailing gateway segments. Confirm it by requesting:

```http
GET {service-root}/
Accept: application/json
OData-Version: 4.0
OData-MaxVersion: 4.01
```

A JSON service document normally contains `value`, whose entries advertise top-level collections, singletons, and function imports. Some protected services expose `$metadata` while restricting the service document, or vice versa; try both before concluding discovery is unavailable.

## Read `$metadata`

Request `{service-root}/$metadata`. XML CSDL is the interoperable default. Build this map before writing a non-trivial query:

- `EntityContainer`: the public surface of entity sets, singletons, and operation imports.
- `EntitySet Name` and `EntityType`: the collection URL and its underlying type.
- `EntityType`, `Key`, `Property`: exact identifier names, key order, EDM types, nullability, precision, and scale.
- `NavigationProperty`: relationship name, target type, collection/singleton cardinality, and containment.
- `ComplexType`, enums, type definitions, inheritance, and open types when relevant.
- Bound/unbound functions when the user asks for computed or provider-defined reads.

Do not guess pluralization, key names, or navigation paths from natural language. Names can be case-sensitive.

## Inspect capability annotations

Look for annotations whose terms begin with `Org.OData.Capabilities.V1`, at the entity container, entity set, or property/navigation target. Common decision-changing terms include:

- `ReadRestrictions` and `ReadByKeyRestrictions`
- `FilterRestrictions`, including non-filterable properties and required properties
- `SortRestrictions`
- `SelectSupport`
- `ExpandRestrictions`
- `SearchRestrictions`
- `CountRestrictions`
- `TopSupported` and `SkipSupported`
- `NavigationRestrictions`
- `IndexableByKey`

Absence of an annotation is not proof that a feature works. It may mean “not advertised”; use a small probe and handle a `4xx` response.

## When metadata is unavailable

Authentication gateways sometimes block metadata, and a provider may publish an OData-shaped endpoint with incomplete CSDL. Use, in order:

1. Provider documentation supplied or identified by the user.
2. The service document.
3. A small collection request such as `EntitySet?$top=1`.
4. Observed response context/type annotations.

Mark inferred field names and types as assumptions. Do not claim general OData portability when provider behavior contradicts its metadata or the protocol.

## Version handling

This skill supports only OData 4.0 and 4.01. Prefer 4.0-compatible URL spelling: lower-case system query options with the `$` prefix. Use 4.01-only constructs only after the service advertises or successfully accepts 4.01. Reject or reroute endpoints identified as OData v1–v3 rather than applying v4 payload or URL rules.
