import PocketBase from "pocketbase";

const POCKETBASE_URL = process.env.POCKETBASE_URL || "http://localhost:8090";
const POCKETBASE_ADMIN_TOKEN = process.env.POCKETBASE_ADMIN_TOKEN || "";
const AI_API_URL = process.env.AI_API_URL || "";
const AI_API_KEY = process.env.AI_API_KEY || "";

const pb = new PocketBase(POCKETBASE_URL);

// Login to PocketBase admin (simplified)
(async () => {
  if (POCKETBASE_ADMIN_TOKEN) {
    await pb.admins.authWithPassword("admin", POCKETBASE_ADMIN_TOKEN);
  }
})();

// Helper: parse inventory command arguments
function parseInventoryArgs(args) {
  const items = [];
  let expirationDate = null;
  let i = 0;
  while (i < args.length) {
    if (args[i] === "expiration") {
      expirationDate = args[i + 1];
      i += 2;
      continue;
    }
    const itemName = args[i];
    const qty = parseInt(args[i + 1], 10);
    if (isNaN(qty)) break;
    items.push({ name: itemName, quantity: qty });
    i += 2;
  }
  return { items, expirationDate };
}

// Dynamic pricing function
function calculateDiscountedPrice(
  cost,
  desiredPrice,
  daysToExpire,
  maxDiscountPercent = 20,
) {
  if (daysToExpire <= 0) return cost;
  const discountStep = maxDiscountPercent / 7;
  const discountPercent = Math.min(
    maxDiscountPercent,
    discountStep * (7 - daysToExpire),
  );
  const discountedPrice = desiredPrice * (1 - discountPercent / 100);
  return discountedPrice < cost ? cost : discountedPrice;
}

// Call external AI api (stub)
async function callAIForecastAPI(itemName, salesData) {
  if (!AI_API_URL || !AI_API_KEY)
    return { forecastedDemand: 10, priceRecommendation: 5.99 };
  // Implement real API call here when ready
  return { forecastedDemand: 10, priceRecommendation: 5.99 };
}

// Main message handler
export async function handleMessage({ from, message, session }) {
  if (!pb.authStore.token) {
    await pb.admins.authWithPassword("admin", POCKETBASE_ADMIN_TOKEN);
  }

  const text = message.trim().toLowerCase();
  const [command, ...args] = text.split(/\s+/);

  if (!["inventory", "sold", "schedule"].includes(command)) {
    return `Unknown command. Available: inventory, sold, schedule`;
  }

  if (command === "inventory") {
    const { items, expirationDate } = parseInventoryArgs(args);
    if (!expirationDate) {
      return "Please provide expiration date as: expiration YYYY-MM-DD";
    }

    for (const item of items) {
      // Get or create item record
      let records = await pb
        .collection("items")
        .getFullList(1, { filter: `name = "${item.name}"` });
      let itemRecord;
      if (records.length === 0) {
        itemRecord = await pb.collection("items").create({
          name: item.name,
          SKU: item.name,
          category: "default",
          cost: 2.0,
          desiredPrice: 5.0,
        });
      } else {
        itemRecord = records[0];
      }
      // Add inventory entry
      await pb.collection("inventoryentries").create({
        itemId: itemRecord.id,
        locationId: "default-location",
        quantity: item.quantity,
        expirationDate: expirationDate,
        addedDate: new Date().toISOString(),
      });
    }
    return `Inventory for items updated.`;
  }

  if (command === "sold") {
    const itemName = args[0];
    const qtySold = parseInt(args[1], 10) || 1;

    let records = await pb
      .collection("items")
      .getFullList(1, { filter: `name = "${itemName}"` });
    if (records.length === 0) return `Item ${itemName} not found.`;
    const itemRecord = records[0];

    await pb.collection("salesrecords").create({
      itemId: itemRecord.id,
      locationId: "default-location",
      quantity: qtySold,
      saleDate: new Date().toISOString(),
      salePrice: itemRecord.desiredPrice,
    });

    let invRec = await pb
      .collection("inventoryentries")
      .getFullList(undefined, {
        filter: `itemId = "${itemRecord.id}" AND quantity > 0`,
        sort: "expirationDate",
      });
    let qtyToDeduct = qtySold;
    for (const entry of invRec) {
      if (qtyToDeduct <= 0) break;
      const deductAmount =
        entry.quantity >= qtyToDeduct ? qtyToDeduct : entry.quantity;
      await pb
        .collection("inventoryentries")
        .update(entry.id, { quantity: entry.quantity - deductAmount });
      qtyToDeduct -= deductAmount;
    }
    return `Recorded sale of ${qtySold} ${itemName}(s).`;
  }

  if (command === "schedule") {
    const today = new Date().toISOString().slice(0, 10);
    const invEntries = await pb
      .collection("inventoryentries")
      .getFullList(undefined, { filter: `expirationDate <= "${today}"` });

    const schedule = [];
    for (let e of invEntries) {
      const item = await pb.collection("items").getOne(e.itemId);
      schedule.push({
        itemName: item.name,
        scheduledQuantity: e.quantity,
        displayPeriod: "morning",
      });
    }

    if (schedule.length === 0) return "No scheduled items today.";

    let text = "Today's Schedule:\n";
    schedule.forEach((e) => {
      text += `${e.itemName}: ${e.scheduledQuantity} (${e.displayPeriod})\n`;
    });
    return text;
  }
}
