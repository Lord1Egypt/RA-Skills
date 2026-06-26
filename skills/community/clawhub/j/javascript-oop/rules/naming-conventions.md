# Naming Conventions

- Use descriptive names.
- Use `camelCase` for values, methods and variables.
- Use `PascalCase` for classes and constructor functions.
- Use `UPPER_SNAKE_CASE` for exported immutable constants.
- Use role suffixes such as `Service`, `Repository`, `Policy`, `UseCase`, `Port`,
  `Specification`, `Mapper`, `Factory`, `Controller`, `View`, `Presenter`, and `State`
  for architectural types.
- Use verb-first behavior names and noun-first value names.

## Example

```js
class InvoiceService {}
class InvoiceRepository {}
class DiscountPolicy {}
class LoadInvoiceUseCase {}
class InvoicePort {}
class InvoiceMapper {}
class TabsController {}
class RunningLightController {}
class TabState {}
export const MAX_RETRY_COUNT = 3;
```

## End Check

- Verify names explain intent without comments.
- Verify case conventions stay consistent across the module.
