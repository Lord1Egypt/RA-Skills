# Classes and Constructors

- Prefer classes as the default home for stateful domain, application, and
  interface-controller behavior.
- Use parameter-object constructors and `#private` collaborators.
- Keep constructors thin: assign collaborators and validate invariants only.
- For browser controllers, move DOM lookup, event binding, and initial render into
  `start()` or `static create()`.
- Move branching or setup into static factories.
- Prefer composition over inheritance; use `extends` only for true subtype contracts.
- Avoid multi-purpose service or controller classes.

## Example

```js
class InvoiceService {
    
    #invoiceRepository;
    #discountPolicy;

    constructor({ invoiceRepository, discountPolicy }) {
        this.#invoiceRepository = invoiceRepository;
        this.#discountPolicy = discountPolicy;
    }

    static create(dependencies) {
        return new InvoiceService(dependencies);
    }

    save(draft) {
        const total = this.#discountPolicy.apply(draft.totalAmount);
        return this.#invoiceRepository.save({ ...draft, totalAmount: total });
    }
}
```

## End Check

- Verify constructors only assign dependencies or validate invariants.
- Verify controller lifecycle work does not leak into constructors.
- Verify setup logic moves to a factory before constructors grow procedural.
- Verify classes own stateful business behavior instead of utility modules.
- Verify `#private` fields reduce boilerplate without hiding real coupling.
