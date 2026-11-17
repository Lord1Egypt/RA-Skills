# Evidence - checkout-empty-state-proof

## Build Summary

The empty-state decision now branches on whether the customer has recoverable saved-cart history. Returning customers see `Restore saved cart`; new carts still see `Continue shopping`.

## AC1 - PASS

`raw/returning-empty-cart.txt` records a returning empty-cart browser check with the saved-cart recovery action visible.

## AC2 - PASS

`raw/new-empty-cart.txt` records a brand-new empty-cart browser check with the existing continue-shopping action visible.

## AC3 - PASS

`raw/checkout-regression.txt` records the checkout regression command passing.
