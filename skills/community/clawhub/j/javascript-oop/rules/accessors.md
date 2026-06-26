# Accessors

- Hide mutable state behind `#private` fields when encapsulation removes boilerplate.
- Prefer intent methods over generic getters and setters.
- Avoid trivial getter/setter pairs that only mirror storage.
- Use accessors for computed, side-effect-free views.
- Keep validation and invariants inside the type.

## Example

```js
class InvoiceDraft {

    #status = "NEW";

    markSubmitted() {
        if (this.#status !== "NEW") {
          throw new Error("Only new drafts can be submitted");
        }
        
        this.#status = "SUBMITTED";
    }

    get isSubmitted() {
        return this.#status === "SUBMITTED";
    }
}
```

## End Check

- Verify callers cannot bypass invariants.
- Verify accessors expose views, not hidden mutations.
- Verify behavior methods replace trivial property mutation APIs.
