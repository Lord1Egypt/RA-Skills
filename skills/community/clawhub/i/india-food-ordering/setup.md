# Setup (first use)

## 1) Confirm vendor connectivity

- Swiggy connector available? yes/no
- Zomato connector available? yes/no
- EatSure connector available? yes/no
- magicpin connector available? yes/no
- ONDC food connector available? yes/no
- Blinkit Bistro / Zepto Cafe connector available? yes/no

If only one is available, run single-vendor mode and disclose this to user.

## 2) Confirm supported actions

Per vendor, mark available:

- search restaurants
- fetch menu
- add to cart
- place order
- booking/cancellation support

## 3) Confirm payment and cancellation behavior

- COD only? yes/no
- online payment supported? yes/no
- cancellable post-order? yes/no/conditional

Always surface these constraints before order confirmation.

## 4) Address labels

Define safe address aliases:

- home -> full address
- office -> full address
- other saved labels

Never infer ambiguous address labels silently.

