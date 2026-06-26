/**
 * Handwrytten MCP Server
 *
 * Exposes the full Handwrytten API as MCP tools so AI assistants
 * like Claude can send real handwritten notes, manage addresses,
 * browse cards/fonts, and more.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { Handwrytten } from "handwrytten";

// ---------------------------------------------------------------------------
// Initialise
// ---------------------------------------------------------------------------

const API_KEY = process.env.HANDWRYTTEN_API_KEY;
if (!API_KEY) {
  console.error(
    "Error: HANDWRYTTEN_API_KEY environment variable is required.\n" +
      "Get your API key at https://www.handwrytten.com/api/"
  );
  process.exit(1);
}

const client = new Handwrytten(API_KEY);

const server = new McpServer(
  {
    name: "handwrytten",
    version: "1.2.0",
  },
  {
    capabilities: {
      tools: {},
    },
    instructions:
      "Handwrytten MCP server — send real handwritten notes at scale using robots with real pens. " +
      "Use list_cards and list_fonts first to discover available options, then send_order to mail a note.",
  }
);

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Wrap a tool handler so errors become MCP error results instead of crashes. */
function ok(content: unknown): { content: { type: "text"; text: string }[] } {
  return {
    content: [{ type: "text" as const, text: JSON.stringify(content, null, 2) }],
  };
}

function err(message: string): { content: { type: "text"; text: string }[]; isError: true } {
  return {
    content: [{ type: "text" as const, text: `Error: ${message}` }],
    isError: true,
  };
}

// ---------------------------------------------------------------------------
// Shared Zod schemas
// ---------------------------------------------------------------------------

const AddressSchema = z.object({
  firstName: z.string().describe("Recipient/sender first name"),
  lastName: z.string().describe("Recipient/sender last name"),
  street1: z.string().describe("Street address line 1"),
  city: z.string().describe("City"),
  state: z.string().describe("State/province code (e.g. 'AZ')"),
  zip: z.string().describe("ZIP/postal code"),
  street2: z.string().optional().describe("Street address line 2 (apt, suite, etc.)"),
  company: z.string().optional().describe("Company name"),
  country: z.string().optional().describe("Country code (default: US)"),
});

// ═══════════════════════════════════════════════════════════════════════════
// ACCOUNT
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "get_user",
  "Get the authenticated Handwrytten user's profile, including credits balance",
  {},
  async () => {
    try {
      const user = await client.auth.getUser();
      return ok(user);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "list_signatures",
  "List the user's saved handwriting signatures for use in orders",
  {},
  async () => {
    try {
      const sigs = await client.auth.listSignatures();
      return ok(sigs);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ═══════════════════════════════════════════════════════════════════════════
// CARDS
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "list_cards",
  "Browse available card/stationery templates. Returns id, title, imageUrl, category for each card. " +
    "Use categoryId=27 for 'My Custom Cards'. Use list_card_categories to discover category IDs. " +
    "Results are paginated — default 20 per page.",
  {
    categoryId: z
      .number()
      .optional()
      .describe(
        "Filter by category ID. Use 27 for 'My Custom Cards'. " +
          "Call list_card_categories to see all options."
      ),
    category: z
      .string()
      .optional()
      .describe(
        "Filter by category name (case-insensitive partial match, e.g. 'thank you', 'birthday', 'custom')"
      ),
    page: z
      .number()
      .optional()
      .describe("Page number (default: 1)"),
    perPage: z
      .number()
      .optional()
      .describe("Results per page (default: 20, max: 50)"),
    query: z
      .string()
      .optional()
      .describe("Search card names (case-insensitive partial match)"),
  },
  async ({ categoryId, category, page, perPage, query }) => {
    try {
      // Fetch all cards and categories in parallel
      const [allCards, categoriesRaw] = await Promise.all([
        client.cards.list(),
        (client as any)._http.get("categories/list") as Promise<any>,
      ]);

      // Build category lookup
      const categories: Record<number, string> = {};
      const catList = (categoriesRaw as any)?.categories ?? [];
      for (const cat of catList) {
        if (cat.id != null && cat.name) categories[cat.id] = cat.name;
      }

      // Resolve category name to ID if provided
      let filterCatId = categoryId;
      if (!filterCatId && category) {
        const lower = category.toLowerCase();
        const match = catList.find(
          (c: any) => c.name && c.name.toLowerCase().includes(lower)
        );
        if (match) filterCatId = match.id;
      }

      // Filter
      let filtered = allCards;
      if (filterCatId != null) {
        filtered = filtered.filter(
          (c) => (c.raw as any).category_id === filterCatId
        );
      }
      if (query) {
        const q = query.toLowerCase();
        filtered = filtered.filter(
          (c) =>
            (c.title && c.title.toLowerCase().includes(q)) ||
            ((c.raw as any).name && String((c.raw as any).name).toLowerCase().includes(q))
        );
      }

      // Paginate
      const pg = Math.max(1, page ?? 1);
      const pp = Math.min(50, Math.max(1, perPage ?? 20));
      const total = filtered.length;
      const totalPages = Math.ceil(total / pp);
      const start = (pg - 1) * pp;
      const pageItems = filtered.slice(start, start + pp);

      // Return slim card objects to stay under size limits
      const results = pageItems.map((c) => ({
        id: c.id,
        title: c.title || (c.raw as any).name,
        category: categories[(c.raw as any).category_id] ?? null,
        categoryId: (c.raw as any).category_id,
        imageUrl: c.imageUrl || c.cover || null,
        orientation: (c.raw as any).orientation,
        closedWidth: (c.raw as any).closed_width,
        closedHeight: (c.raw as any).closed_height,
      }));

      return ok({
        cards: results,
        pagination: { page: pg, perPage: pp, total, totalPages },
      });
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "get_card",
  "Get details of a specific card template by ID",
  { cardId: z.string().describe("The card template ID") },
  async ({ cardId }) => {
    try {
      const card = await client.cards.get(cardId);
      return ok(card);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "list_card_categories",
  "Get available card categories (e.g. Thank You, Birthday, My Custom Cards). " +
    "Use the returned category ID with list_cards to filter.",
  {},
  async () => {
    try {
      const data = await (client as any)._http.get("categories/list") as any;
      const categories = (data?.categories ?? []).map((c: any) => ({
        id: c.id,
        name: c.name,
        slug: c.slug,
      }));
      return ok(categories);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ═══════════════════════════════════════════════════════════════════════════
// FONTS
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "list_fonts",
  "Browse available handwriting fonts/styles for orders. Returns id, name, label, previewUrl.",
  {},
  async () => {
    try {
      const fonts = await client.fonts.list();
      return ok(fonts);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "list_customizer_fonts",
  "Browse printed/typeset fonts available for custom card text zones (header, footer, main, back). Different from handwriting fonts.",
  {},
  async () => {
    try {
      const fonts = await client.fonts.listForCustomizer();
      return ok(fonts);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ═══════════════════════════════════════════════════════════════════════════
// GIFT CARDS
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "list_gift_cards",
  "Browse available gift card products with their denominations (price points). Include a denominationId in an order to attach a gift card.",
  {},
  async () => {
    try {
      const gcs = await client.giftCards.list();
      return ok(gcs);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ═══════════════════════════════════════════════════════════════════════════
// INSERTS
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "list_inserts",
  "Browse available card inserts (business cards, flyers, etc.) that can be included in an order",
  {
    includeHistorical: z
      .boolean()
      .optional()
      .describe("If true, also return discontinued inserts"),
  },
  async ({ includeHistorical }) => {
    try {
      const inserts = await client.inserts.list({ includeHistorical });
      return ok(inserts);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ═══════════════════════════════════════════════════════════════════════════
// QR CODES
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "list_qr_codes",
  "List QR codes associated with the account",
  {},
  async () => {
    try {
      const qrs = await client.qrCodes.list();
      return ok(qrs);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "create_qr_code",
  "Create a new QR code for use on custom cards",
  {
    name: z.string().describe("Display name for the QR code"),
    url: z.string().describe("URL the QR code should link to"),
    iconId: z.number().optional().describe("Optional icon ID"),
    webhookUrl: z.string().optional().describe("Optional webhook URL for scan notifications"),
  },
  async (params) => {
    try {
      const qr = await client.qrCodes.create(params);
      return ok(qr);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "delete_qr_code",
  "Delete a QR code",
  { qrCodeId: z.number().describe("ID of the QR code to delete") },
  async ({ qrCodeId }) => {
    try {
      const result = await client.qrCodes.delete(qrCodeId);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "list_qr_code_frames",
  "Browse available decorative frames for QR codes on custom cards",
  {},
  async () => {
    try {
      const frames = await client.qrCodes.frames();
      return ok(frames);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ═══════════════════════════════════════════════════════════════════════════
// ADDRESS BOOK
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "list_recipients",
  "List saved recipient addresses from the address book",
  {},
  async () => {
    try {
      const recipients = await client.addressBook.listRecipients();
      return ok(recipients);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "add_recipient",
  "Save a new recipient address to the address book. Returns the saved address ID.",
  {
    firstName: z.string().describe("First name"),
    lastName: z.string().describe("Last name"),
    street1: z.string().describe("Street address"),
    city: z.string().describe("City"),
    state: z.string().describe("State/province code"),
    zip: z.string().describe("ZIP/postal code"),
    street2: z.string().optional().describe("Address line 2"),
    company: z.string().optional().describe("Company name"),
    countryId: z.string().optional().describe("Country code"),
    birthday: z.string().optional().describe("Birthday (YYYY-MM-DD)"),
    anniversary: z.string().optional().describe("Anniversary (YYYY-MM-DD)"),
  },
  async (params) => {
    try {
      const id = await client.addressBook.addRecipient(params);
      return ok({ addressId: id, message: "Recipient saved successfully" });
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "update_recipient",
  "Update an existing saved recipient address",
  {
    addressId: z.number().describe("ID of the address to update"),
    firstName: z.string().optional().describe("First name"),
    lastName: z.string().optional().describe("Last name"),
    street1: z.string().optional().describe("Street address"),
    city: z.string().optional().describe("City"),
    state: z.string().optional().describe("State/province code"),
    zip: z.string().optional().describe("ZIP/postal code"),
    street2: z.string().optional().describe("Address line 2"),
    company: z.string().optional().describe("Company name"),
    countryId: z.string().optional().describe("Country code"),
    birthday: z.string().optional().describe("Birthday (YYYY-MM-DD)"),
    anniversary: z.string().optional().describe("Anniversary (YYYY-MM-DD)"),
  },
  async (params) => {
    try {
      const id = await client.addressBook.updateRecipient(params);
      return ok({ addressId: id, message: "Recipient updated successfully" });
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "delete_recipient",
  "Delete one or more saved recipient addresses",
  {
    addressId: z.number().optional().describe("Single address ID to delete"),
    addressIds: z
      .array(z.number())
      .optional()
      .describe("Array of address IDs for batch delete"),
  },
  async (params) => {
    try {
      const result = await client.addressBook.deleteRecipient(params);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "list_senders",
  "List saved sender (return) addresses from the address book",
  {},
  async () => {
    try {
      const senders = await client.addressBook.listSenders();
      return ok(senders);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "add_sender",
  "Save a new sender (return) address to the address book. Returns the saved address ID.",
  {
    firstName: z.string().describe("First name"),
    lastName: z.string().describe("Last name"),
    street1: z.string().describe("Street address"),
    city: z.string().describe("City"),
    state: z.string().describe("State/province code"),
    zip: z.string().describe("ZIP/postal code"),
    street2: z.string().optional().describe("Address line 2"),
    company: z.string().optional().describe("Company name"),
    countryId: z.string().optional().describe("Country code"),
    default: z.boolean().optional().describe("Set as the default return address"),
  },
  async (params) => {
    try {
      const id = await client.addressBook.addSender(params);
      return ok({ addressId: id, message: "Sender saved successfully" });
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "delete_sender",
  "Delete one or more saved sender (return) addresses",
  {
    addressId: z.number().optional().describe("Single address ID to delete"),
    addressIds: z
      .array(z.number())
      .optional()
      .describe("Array of address IDs for batch delete"),
  },
  async (params) => {
    try {
      const result = await client.addressBook.deleteSender(params);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "list_countries",
  "Get all countries supported by Handwrytten for mailing addresses",
  {},
  async () => {
    try {
      const countries = await client.addressBook.countries();
      return ok(countries);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "list_states",
  "Get states/provinces for a country",
  {
    countryCode: z
      .string()
      .optional()
      .describe("Country code (default: US)"),
  },
  async ({ countryCode }) => {
    try {
      const states = await client.addressBook.states(countryCode);
      return ok(states);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ═══════════════════════════════════════════════════════════════════════════
// ORDERS — The main event!
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "send_order",
  "Send a real handwritten note via Handwrytten. This is the primary tool — it places " +
    "an order that results in a physical card being written by a robot with a real pen " +
    "and mailed to the recipient. Use list_cards and list_fonts first to get valid IDs. " +
    "The recipient can be an inline address object or a saved address ID number. " +
    "For bulk sends, pass an array of recipients.",
  {
    cardId: z.string().describe("Card template ID (from list_cards)"),
    font: z.string().describe("Handwriting font ID or label (from list_fonts)"),
    message: z.string().optional().describe("The handwritten message body"),
    wishes: z.string().optional().describe("Closing wishes (e.g. 'Best,\\nThe Team')"),
    recipient: z
      .union([
        AddressSchema,
        z.number().describe("Saved recipient address ID"),
        z.array(
          z.union([
            AddressSchema.extend({
              message: z.string().optional().describe("Per-recipient message override"),
              wishes: z.string().optional().describe("Per-recipient wishes override"),
            }),
            z.number().describe("Saved recipient address ID"),
          ])
        ),
      ])
      .describe("Recipient — an address object, saved address ID, or array for bulk"),
    sender: z
      .union([
        AddressSchema,
        z.number().describe("Saved sender address ID"),
      ])
      .optional()
      .describe("Return address — an address object or saved sender ID"),
    denominationId: z
      .number()
      .optional()
      .describe("Gift card denomination ID to include (from list_gift_cards)"),
    insertId: z
      .number()
      .optional()
      .describe("Insert ID to include (from list_inserts)"),
    signatureId: z
      .number()
      .optional()
      .describe("Signature ID to use (from list_signatures)"),
    dateSend: z
      .string()
      .optional()
      .describe("Schedule send date (YYYY-MM-DD). Omit to send immediately."),
    clientMetadata: z
      .string()
      .optional()
      .describe("Your own reference string for tracking"),
  },
  async (params) => {
    try {
      const result = await client.orders.send(params as any);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "get_order",
  "Get details of a specific order by ID, including status and tracking",
  { orderId: z.string().describe("The order ID") },
  async ({ orderId }) => {
    try {
      const order = await client.orders.get(orderId);
      return ok(order);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "list_orders",
  "List orders with pagination",
  {
    page: z.number().optional().describe("Page number (default: 1)"),
    perPage: z.number().optional().describe("Results per page"),
  },
  async (params) => {
    try {
      const orders = await client.orders.list(params);
      return ok(orders);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "list_past_baskets",
  "List previously submitted order baskets",
  {
    page: z.number().optional().describe("Page number"),
  },
  async (params) => {
    try {
      const baskets = await client.orders.listPastBaskets(params);
      return ok(baskets);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ═══════════════════════════════════════════════════════════════════════════
// BASKET (advanced multi-step workflow)
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "basket_add_order",
  "Add an order to the basket (multi-step workflow). Use send_order instead for single-step sends.",
  {
    cardId: z.string().describe("Card template ID"),
    font: z.string().optional().describe("Handwriting font ID"),
    message: z.string().optional().describe("The handwritten message"),
    wishes: z.string().optional().describe("Closing wishes"),
    addresses: z
      .array(
        z.object({
          firstName: z.string(),
          lastName: z.string(),
          street1: z.string(),
          city: z.string(),
          state: z.string(),
          zip: z.string(),
          street2: z.string().optional(),
          company: z.string().optional(),
          message: z.string().optional().describe("Per-recipient message override"),
        })
      )
      .optional()
      .describe("Recipient addresses with optional per-recipient messages"),
    addressIds: z
      .array(z.number())
      .optional()
      .describe("Saved recipient address IDs"),
    returnAddressId: z.number().optional().describe("Saved sender address ID"),
    denominationId: z.number().optional().describe("Gift card denomination ID"),
    insertId: z.number().optional().describe("Insert ID"),
    signatureId: z.number().optional().describe("Signature ID"),
    dateSend: z.string().optional().describe("Scheduled send date (YYYY-MM-DD)"),
    clientMetadata: z.string().optional().describe("Your reference string"),
  },
  async (params) => {
    try {
      const result = await client.basket.addOrder(params as any);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "basket_send",
  "Submit the current basket for processing — actually sends all orders in the basket",
  {
    couponCode: z.string().optional().describe("Coupon code"),
    testMode: z.boolean().optional().describe("If true, orders are not actually sent"),
  },
  async (params) => {
    try {
      const result = await client.basket.send(params);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "basket_list",
  "List all items currently in the basket",
  {},
  async () => {
    try {
      const items = await client.basket.list();
      return ok(items);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "basket_count",
  "Get the number of items currently in the basket",
  {},
  async () => {
    try {
      const count = await client.basket.count();
      return ok({ count });
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "basket_remove",
  "Remove a single item from the basket",
  { basketId: z.number().describe("Basket item ID to remove") },
  async ({ basketId }) => {
    try {
      const result = await client.basket.remove(basketId);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "basket_clear",
  "Remove all items from the basket",
  {},
  async () => {
    try {
      const result = await client.basket.clear();
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ═══════════════════════════════════════════════════════════════════════════
// CUSTOM CARDS
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "list_custom_card_dimensions",
  "Get available dimensions for custom card designs (format, orientation, size)",
  {
    format: z
      .string()
      .optional()
      .describe("Filter by format: 'flat' or 'folded'"),
    orientation: z
      .string()
      .optional()
      .describe("Filter by orientation: 'portrait' or 'landscape'"),
  },
  async (params) => {
    try {
      const dims = await client.customCards.dimensions(params);
      return ok(dims);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "upload_custom_image",
  "Upload a custom image (cover or logo) for use in custom card designs",
  {
    url: z.string().describe("Publicly accessible URL of the image (JPEG/PNG/GIF)"),
    imageType: z
      .enum(["cover", "logo"])
      .describe("'cover' for full-bleed front/back, 'logo' for writing-side logo"),
  },
  async (params) => {
    try {
      const img = await client.customCards.uploadImage(params);
      return ok(img);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "check_custom_image",
  "Check if an uploaded image meets quality requirements for custom cards",
  {
    imageId: z.number().describe("Image ID to check"),
    cardId: z.number().optional().describe("Optional card ID for dimension-specific checks"),
  },
  async ({ imageId, cardId }) => {
    try {
      const result = await client.customCards.checkImage(imageId, cardId);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "list_custom_images",
  "List previously uploaded custom images",
  {
    imageType: z
      .enum(["cover", "logo"])
      .optional()
      .describe("Filter by image type"),
  },
  async ({ imageType }) => {
    try {
      const images = await client.customCards.listImages(imageType);
      return ok(images);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "delete_custom_image",
  "Delete an uploaded custom image",
  { imageId: z.number().describe("Image ID to delete") },
  async ({ imageId }) => {
    try {
      const result = await client.customCards.deleteImage(imageId);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "create_custom_card",
  "Create a custom card design from uploaded images and text zones.\n\n" +
    "IMPORTANT — Each writing-side zone (header/main/footer) and the back side has a 'type' field:\n" +
    "  type='logo' → displays a logo image (must also provide the matching logoId + sizePercent)\n" +
    "  type='text' → displays printed text (provide text + fontId)\n" +
    "  If you set a logoId without setting the type to 'logo', the logo will NOT render.\n\n" +
    "FLAT CARDS (dimension_id=1 or 2) — writing-side logo example:\n" +
    "  headerLogoId=IMG_ID, headerLogoSizePercent=80, headerType='logo'\n\n" +
    "FOLDED CARDS (dimension_id=3) — back/writing side is REQUIRED:\n" +
    "  backLogoId=IMG_ID, backSizePercent=20, backType='logo', backVerticalAlign='center'\n\n" +
    "Upload images first with upload_custom_image:\n" +
    "  imageType='cover' → full-bleed front covers (use with coverId)\n" +
    "  imageType='logo'  → logos for the writing side (use with headerLogoId/mainLogoId/footerLogoId/backLogoId)",
  {
    name: z.string().describe("Name for the custom card"),
    dimensionId: z.string().describe("Dimension ID (from list_custom_card_dimensions)"),
    coverId: z.number().optional().describe("Front cover image ID (from upload_custom_image with imageType='cover')"),

    // --- Writing-side header zone ---
    headerType: z
      .enum(["logo", "text"])
      .optional()
      .describe("Header zone content type. MUST be 'logo' when using headerLogoId, or 'text' for printed text."),
    headerText: z.string().optional().describe("Header zone printed text (when headerType='text')"),
    headerFontId: z.string().optional().describe("Header font ID (from list_customizer_fonts)"),
    headerLogoId: z
      .number()
      .optional()
      .describe("Header zone logo image ID. MUST set headerType='logo' for this to render."),
    headerLogoSizePercent: z.number().optional().describe("Header logo size (1-100)"),

    // --- Writing-side main zone ---
    mainType: z
      .enum(["logo", "text"])
      .optional()
      .describe("Main zone content type. MUST be 'logo' when using mainLogoId, or 'text' for printed text."),
    mainText: z.string().optional().describe("Main zone printed text (when mainType='text')"),
    mainFontId: z.string().optional().describe("Main zone font ID"),
    mainLogoId: z
      .number()
      .optional()
      .describe("Main zone logo image ID. MUST set mainType='logo' for this to render."),
    mainLogoSizePercent: z.number().optional().describe("Main logo size (1-100)"),

    // --- Writing-side footer zone ---
    footerType: z
      .enum(["logo", "text"])
      .optional()
      .describe("Footer zone content type. MUST be 'logo' when using footerLogoId, or 'text' for printed text."),
    footerText: z.string().optional().describe("Footer zone printed text (when footerType='text')"),
    footerFontId: z.string().optional().describe("Footer zone font ID"),
    footerLogoId: z
      .number()
      .optional()
      .describe("Footer zone logo image ID. MUST set footerType='logo' for this to render."),
    footerLogoSizePercent: z.number().optional().describe("Footer logo size (1-100)"),

    // --- Back side (REQUIRED for folded cards, optional for flat) ---
    backLogoId: z
      .number()
      .optional()
      .describe(
        "Image ID for the back/writing side (from upload_custom_image). " +
          "REQUIRED for folded cards (dimension_id=3). Must be paired with backType."
      ),
    backType: z
      .enum(["logo", "cover"])
      .optional()
      .describe(
        "Type of back side content. REQUIRED when backLogoId is provided. " +
          "'logo' = sized/aligned logo image; 'cover' = full-bleed cover image."
      ),
    backSizePercent: z
      .number()
      .optional()
      .describe("Back logo size as percentage (1-100). Only used when backType='logo'."),
    backVerticalAlign: z
      .enum(["top", "center", "bottom"])
      .optional()
      .describe("Vertical alignment of back logo. Only used when backType='logo'."),
    backCoverId: z.number().optional().describe("Back cover image ID (alternative to backLogoId for full-bleed backs)"),
    backText: z.string().optional().describe("Back side printed text"),
    backFontId: z.number().optional().describe("Back side font ID"),

    // --- QR code ---
    qrCodeId: z.number().optional().describe("QR code ID to attach"),
    qrCodeLocation: z
      .enum(["header", "footer", "main"])
      .optional()
      .describe("Where to place the QR code"),
    qrCodeSizePercent: z.number().optional().describe("QR code size (1-100)"),
    qrCodeAlign: z.string().optional().describe("QR code alignment (left, center, right)"),
    qrCodeFrameId: z.number().optional().describe("QR code frame ID"),
  },
  async (params) => {
    try {
      const card = await client.customCards.create(params as any);
      return ok(card);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "get_custom_card",
  "Get details of a custom card design",
  { cardId: z.number().describe("Custom card ID") },
  async ({ cardId }) => {
    try {
      const card = await client.customCards.get(cardId);
      return ok(card);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

server.tool(
  "delete_custom_card",
  "Delete a custom card design",
  { cardId: z.number().describe("Custom card ID to delete") },
  async ({ cardId }) => {
    try {
      const result = await client.customCards.delete(cardId);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ═══════════════════════════════════════════════════════════════════════════
// PROSPECTING
// ═══════════════════════════════════════════════════════════════════════════

server.tool(
  "calculate_targets",
  "Calculate prospecting targets in a geographic area by ZIP code and radius",
  {
    zipCode: z.string().describe("Center ZIP code"),
    radiusMiles: z
      .number()
      .optional()
      .describe("Search radius in miles"),
  },
  async (params) => {
    try {
      const result = await client.prospecting.calculateTargets(params);
      return ok(result);
    } catch (e: any) {
      return err(e.message);
    }
  }
);

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Handwrytten MCP server running on stdio");
}

main().catch((e) => {
  console.error("Fatal error:", e);
  process.exit(1);
});
