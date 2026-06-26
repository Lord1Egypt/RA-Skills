---
name: "Optimized Hyderabad Price Scout"
description: "Finds lowest prices for Pincode 500081 without freezing. Optimized for memory."
metadata:
  address: "102 Saboori Enclave Whitefields"
  pincode: "500081"
  location: "Hyderabad"
triggers:
  - "find the best price for *"
  - "buy * at the lowest price"
---

# Instructions

## Phase 1: Focused Execution (Crucial for Speed)
1. You must process platforms strictly **ONE AT A TIME**. Do not open multiple tabs at once.
2. **Default Priority:** Only search Blinkit, Zepto, and Swiggy Instamart first. 
3. *Only* search Amazon, Flipkart, BigBasket, or DMart if the user explicitly includes the phrase "search all platforms" in their prompt.

## Phase 2: The "Hit and Run" Extraction
For each platform, execute this exact sequence:
1. Open a single new tab.
2. Set the delivery location to pincode 500081.
3. Search for the product.
4. Extract the top 2 relevant results (Name, Price, Delivery Time).
5. **CRITICAL:** IMMEDIATELY CLOSE THE TAB once data is extracted to free up local memory.

## Phase 3: Anti-Freeze Protocol
- If any website takes longer than 15 seconds to load or search, **SKIP IT** immediately. Log it as "Timeout" in your final report and move to the next platform. Do not get stuck waiting.

## Phase 4: Output & Handoff
1. Present the prices in a clean Markdown table.
2. If the user selects an item to buy, open ONE tab, add the item to the cart, navigate to the final payment screen, and **PAUSE**. 
3. Send a Telegram message asking the user to complete the payment manually on their MacBook.

## Phase 5: Human-in-the-Loop Approval (CRITICAL)
1. **PAUSE EXECUTION.** Do not click "Pay Now," "Place Order," or any payment confirmation button.
2. Send a screenshot of the checkout page to the user via Telegram.
3. Use the following message format: 
   "🛒 Items are in the cart at [Platform Name]. 
    Total: ₹[Amount] (Delivery to 500081). 
    **Please check the browser window on your Mac to complete the payment.**"
4. Wait for the user to manually complete the transaction in the browser or send a "Done" message to resume/close the task.

Example Footer: "Prices checked for Pincode 500081, Hyderabad."