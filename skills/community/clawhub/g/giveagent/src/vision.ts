import { Condition, Category, Size, SkillContext } from "./types.js";

export interface ItemDescription {
  name: string;
  nameEn: string;
  condition: Condition;
  category: Category;
  estimatedSize: Size;
  notes: string;
}

export interface VisionProvider {
  describeItem(imageUrl: string): Promise<ItemDescription>;
}

/**
 * Delegates to the OpenClaw runtime's describeImage() function.
 * Parses the structured output into an ItemDescription.
 */
export class OpenClawVisionProvider implements VisionProvider {
  private ctx: SkillContext;

  constructor(ctx: SkillContext) {
    this.ctx = ctx;
  }

  async describeItem(imageUrl: string): Promise<ItemDescription> {
    if (!this.ctx.describeImage) {
      throw new Error("Vision not available in current OpenClaw runtime");
    }

    const description = await this.ctx.describeImage(imageUrl);
    return this.parseDescription(description);
  }

  private parseDescription(raw: string): ItemDescription {
    // Parse structured output from vision API
    // Expected format is a JSON-like response with item details
    try {
      const parsed = JSON.parse(raw);
      return {
        name: parsed.name || "Unknown item",
        nameEn: parsed.nameEn || parsed.name || "Unknown item",
        condition: this.validateCondition(parsed.condition) || "Good",
        category: this.validateCategory(parsed.category) || "other",
        estimatedSize: this.validateSize(parsed.estimatedSize) || "Medium",
        notes: parsed.notes || "",
      };
    } catch {
      // If not JSON, treat as plain text description
      return {
        name: raw.split("\n")[0] || "Unknown item",
        nameEn: raw.split("\n")[0] || "Unknown item",
        condition: "Good",
        category: "other",
        estimatedSize: "Medium",
        notes: raw,
      };
    }
  }

  private validateCondition(value: string): Condition | null {
    const valid: Condition[] = ["New", "Like New", "Good", "Fair", "For Parts"];
    return valid.includes(value as Condition) ? (value as Condition) : null;
  }

  private validateCategory(value: string): Category | null {
    const valid: Category[] = [
      "furniture", "electronics", "clothing", "books", "kitchen",
      "kids", "sports", "home", "garden", "office", "media", "other",
    ];
    return valid.includes(value as Category) ? (value as Category) : null;
  }

  private validateSize(value: string): Size | null {
    const valid: Size[] = ["Pocket", "Small", "Medium", "Large", "XL", "Furniture-sized"];
    return valid.includes(value as Size) ? (value as Size) : null;
  }
}

/**
 * Fallback when vision is not available.
 * Returns a template asking the user to fill in details manually.
 */
export class FallbackVisionProvider implements VisionProvider {
  async describeItem(_imageUrl: string): Promise<ItemDescription> {
    return {
      name: "",
      nameEn: "",
      condition: "Good",
      category: "other",
      estimatedSize: "Medium",
      notes: "Vision not available. Please describe the item manually.",
    };
  }
}

/**
 * Factory function to create the appropriate vision provider.
 */
export function createVisionProvider(ctx: SkillContext): VisionProvider {
  if (ctx.describeImage) {
    return new OpenClawVisionProvider(ctx);
  }
  return new FallbackVisionProvider();
}
