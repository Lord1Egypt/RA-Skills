# SOLID and Structure

- Apply SRP to classes, modules, and functions.
- Extend behavior with policies or strategies.
- Keep ports small, adapters replaceable, and dependencies inward.
- Preserve subtype contracts.
- Keep `domain`, `application`, `infrastructure`, and `interface` layers explicit.
- Treat browser controllers as interface-layer coordinators that translate DOM events into
  intent methods or use-case calls.
- Use a composition root to wire concrete repositories, policies, adapters, and
  controllers.

## Example

```js
class CheckoutService {
    
    #discountPolicy;
    #orderRepository;

    constructor({ discountPolicy, orderRepository }) {
        this.#discountPolicy = discountPolicy;
        this.#orderRepository = orderRepository;
    }

    async checkout(order) {
        return this.#orderRepository.save({
            ...order,
            total: this.#discountPolicy.apply(order.total),
        });
    }
}
```

## End Check

- Verify business rules do not depend on infrastructure details.
- Verify composition wiring happens at the edge, not inside domain behavior.
- Verify controllers stay in the `interface` layer and do not absorb domain logic.
- Verify interfaces stay smaller than their implementations.
- Verify new behavior is added with policies or adapters, not core rewrites.
