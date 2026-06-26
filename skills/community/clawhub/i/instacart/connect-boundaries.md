# Connect Boundaries - Instacart

## Do Not Confuse These Products

Developer Platform and Connect are not interchangeable.

## Developer Platform

Use Developer Platform when the goal is:
- recipe pages
- shopping-list pages
- nearby retailer lookup
- lightweight AI or app handoff into Instacart Marketplace

## Connect

Use Connect when the goal is:
- branded ecommerce experiences
- delivery or pickup scheduling
- full-service shopping
- order tracking and post-checkout experiences
- sandboxed callbacks and fulfillment testing

Connect docs position it for branded sites that need fulfillment, post-checkout, sandbox simulation, and broader commerce workflows.

## Routing Rule

If the user says any of these, route to Connect:
- order lifecycle
- delivery windows
- callbacks or webhooks
- post-checkout page
- sandbox order events
- retailer or enterprise fulfillment integration

If the user only needs a linkable grocery page or agent-generated shopping list, stay on Developer Platform.

## Practical Consequence

Bad routing wastes time:
- wrong auth model
- wrong expectations about checkout ownership
- wrong environment and support path
- unnecessary engineering overhead
