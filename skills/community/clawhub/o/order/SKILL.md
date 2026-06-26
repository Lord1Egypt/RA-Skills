---
name: android-order
description: >-
  Order food/drinks (点餐) on an Android device paired as an OpenClaw node.
  Uses in-app menu and cart; add goods, view cart, submit order (demo, no real payment).
version: 1.0.0
user-invocable: true

metadata:
  openclaw:
    capabilities: ["order"]
    commands:
      - name: order.getGoods
        description: Get the menu / goods list (id, name, price).
        params: []
      - name: order.getSelectedGoods
        description: Get current cart / selected items.
        params: []
      - name: order.addGoods
        description: Add a product to the cart by id or name (fuzzy). Default quantity 1.
        params:
          - name: id
            type: string
            description: Goods ID from the menu (e.g. "1").
          - name: name
            type: string
            description: Goods name, supports fuzzy match (e.g. "拿铁", "美式").
          - name: quantity
            type: string
            description: Quantity, default "1".
      - name: order.removeGoods
        description: Remove a product from the cart by id or name.
        params:
          - name: id
            type: string
            description: Goods ID.
          - name: name
            type: string
            description: Goods name (fuzzy).
          - name: quantity
            type: string
            description: Quantity to remove, default "1".
      - name: order.clearGoods
        description: Clear all items in the cart.
        params: []
      - name: order.submitOrder
        description: Submit the current cart as an order (demo; no real payment).
        params: []
      - name: order.batchAddGoods
        description: Add multiple items at once. list is JSON array [{"id":"1","quantity":2},...].
        params:
          - name: list
            type: string
            description: JSON array of objects with id and quantity.
---

# Android Order Skill (点餐)

This skill uses the paired Android device (`OpenClaw SMS Demo` app with order capability) to manage an in-app menu and cart: get menu, add/remove items, view cart, submit order. Inspired by EdgeOSToolService (MEOW PAY); implementation is in-memory on the device (demo, no real POS backend).

## When to use this skill

- User asks to order food/drinks, view menu, add to cart, or submit an order on the paired Android device: use the `order.*` commands below.

## Commands overview

| Command | Description |
|--------|-------------|
| `order.getGoods` | Return menu (id, name, priceCents, price). |
| `order.getSelectedGoods` | Return current cart with quantities and subtotals. |
| `order.addGoods` | Add by `id` or `name` (and optional `quantity`). |
| `order.removeGoods` | Remove by `id` or `name` (and optional `quantity`). |
| `order.clearGoods` | Clear cart. |
| `order.submitOrder` | Submit cart as order; returns summary (demo only). |
| `order.batchAddGoods` | Add multiple items: `list` = `[{"id":"1","quantity":2},...]`. |

## How to call the underlying commands

Invoke via the OpenClaw gateway node invoke API:

- **command**: one of `order.getGoods`, `order.getSelectedGoods`, `order.addGoods`, `order.removeGoods`, `order.clearGoods`, `order.submitOrder`, `order.batchAddGoods`.
- **paramsJSON**: JSON object string, or `null` for no-param commands.

### order.getGoods

- `command`: `"order.getGoods"`
- `paramsJSON`: `null` or `"{}"`
- Success: payload is a JSON array of `{ "id", "name", "priceCents", "price" }`.

### order.getSelectedGoods

- `command`: `"order.getSelectedGoods"`
- `paramsJSON`: `null` or `"{}"`
- Success: payload is a JSON array of cart items with `id`, `name`, `quantity`, `priceCents`, `subtotalCents`.

### order.addGoods

- `command`: `"order.addGoods"`
- `paramsJSON`: provide **id** or **name** (or both); optional **quantity** (default 1).

  ```json
  { "id": "1", "quantity": "2" }
  ```
  or
  ```json
  { "name": "拿铁", "quantity": "1" }
  ```

- Success: payload includes `success: true` and `message` (e.g. "已添加 拿铁 x1").

### order.removeGoods

- `command`: `"order.removeGoods"`
- `paramsJSON`: same shape as addGoods (`id` or `name`, optional `quantity`).

### order.clearGoods

- `command`: `"order.clearGoods"`
- `paramsJSON`: `null` or `"{}"`.

### order.submitOrder

- `command`: `"order.submitOrder"`
- `paramsJSON`: `null` or `"{}"`.
- Success: payload includes `success`, `message`, `totalCents`, `items`. Cart is cleared after submit.
- Error: `CART_EMPTY` if cart is empty.

### order.batchAddGoods

- `command`: `"order.batchAddGoods"`
- `paramsJSON`: `{ "list": "[{\"id\":\"1\",\"quantity\":2},{\"id\":\"2\",\"quantity\":1}]" }`
- Success: payload includes `success` and `message` (e.g. "已批量添加 2 项").

## Error handling

- **GOODS_NOT_FOUND**: No menu item matched the given id or name. Suggest calling `order.getGoods` to see the menu.
- **NOT_IN_CART**: Item not in cart when removing.
- **CART_EMPTY**: Cannot submit when cart is empty.
- **INVALID_REQUEST**: Missing or malformed params (e.g. empty `list` for batchAddGoods).

## Demo menu (default on device)

The in-app menu includes items such as: 拿铁, 美式, 卡布奇诺, 三明治, 沙拉, 蛋糕 (with ids "1"–"6"). Use `order.getGoods` to get the current list and prices.

## Safety notes

- This is a demo flow: submit order does not charge or send to a real POS. Do not expose as real payment.
- Prefer confirming with the user before submitting an order (e.g. read back cart and total).
