/**
 * Identity Parser — Extract structured identity data from workspace .md files
 * 
 * Reads USER.md, COMPANY.md, projects/objectifs.md to build a semantic profile:
 *   - Who is the human (name, role, location, timezone)
 *   - What projects are active (daily, paused, backlog)
 *   - What matters most (priorities, preferences, values)
 * 
 * Used to calculate relevance_weight for facts during extraction.
 */

import fs from "fs";
import path from "path";

export interface Identity {
  human: {
    name: string;
    role: string;
    location: string;
    timezone: string;
  };
  priorities: {
    business: number;
    product: number;
    internal_tools: number;
    infrastructure: number;
  };
  activeProjects: Record<string, {
    weight: number;
    status: "daily" | "active" | "paused" | "backlog";
    type: "product" | "revenue" | "internal_tool" | "infrastructure";
  }>;
  preferences: string[];
  triggers: {
    frustration: string[];
    satisfaction: string[];
    urgency: string[];
  };
}

export class IdentityParser {
  private workspaceRoot: string;
  private cachedIdentity: Identity | null = null;

  constructor(workspaceRoot: string) {
    this.workspaceRoot = workspaceRoot;
  }

  /**
   * Parse identity from .md files (cached, rebuild on demand)
   */
  parse(): Identity {
    if (this.cachedIdentity) return this.cachedIdentity;

    const userMd = this.readFile("USER.md");
    const companyMd = this.readFile("COMPANY.md");
    const objectivesMd = this.readFile("projects/objectifs.md");

    // Extract human info from USER.md
    const human = this.extractHuman(userMd);

    // Extract priorities (business > product > tools > infra)
    const priorities = {
      business: 1.0,
      product: 0.9,
      internal_tools: 0.6,
      infrastructure: 0.4,
    };

    // Extract active projects from COMPANY.md + objectifs.md
    const activeProjects = this.extractProjects(companyMd, objectivesMd);

    // Extract preferences from USER.md
    const preferences = this.extractPreferences(userMd);

    // Extract trigger words from USER.md
    const triggers = this.extractTriggers(userMd);

    this.cachedIdentity = {
      human,
      priorities,
      activeProjects,
      preferences,
      triggers,
    };

    return this.cachedIdentity;
  }

  /**
   * Calculate relevance weight for a fact (0.0 - 1.0)
   * Higher weight = more important to recall
   */
  calculateRelevance(fact: string, category: string): number {
    const identity = this.parse();
    let weight = 0.5; // default

    // Boost if fact mentions the human by name
    if (fact.toLowerCase().includes(identity.human.name.toLowerCase())) {
      weight += 0.2;
    }

    // Boost based on project mentions
    for (const [projectName, project] of Object.entries(identity.activeProjects)) {
      const nameNormalized = projectName.toLowerCase();
      if (fact.toLowerCase().includes(nameNormalized)) {
        weight += project.weight * 0.4; // Scale by project importance
        break; // Only count first match
      }
    }

    // Boost based on category importance
    if (category === "preference" || category === "preference_travail" || category === "preference_communication") {
      weight += 0.3; // Preferences are high priority
    } else if (category === "erreur" || category === "erreur_critique") {
      weight += 0.2; // Errors matter
    } else if (category === "objectif" || category.startsWith("objectif_")) {
      weight += 0.25; // Objectives matter
    }

    // Boost if fact is about business/product (not internal tooling)
    const lowerFact = fact.toLowerCase();
    if (lowerFact.includes("client") || lowerFact.includes("ca ") || lowerFact.includes("chiffre") || lowerFact.includes("facture")) {
      weight += identity.priorities.business * 0.3;
    } else if (lowerFact.includes("memoria") || lowerFact.includes("plugin") || lowerFact.includes("openclaw")) {
      weight += identity.priorities.internal_tools * 0.2; // Lower priority
    }

    // Cap at 1.0
    return Math.min(weight, 1.0);
  }

  /**
   * Invalidate cache (call when .md files change)
   */
  invalidateCache(): void {
    this.cachedIdentity = null;
  }

  // ─── Private Helpers ───

  private readFile(relativePath: string): string {
    try {
      const fullPath = path.join(this.workspaceRoot, relativePath);
      return fs.readFileSync(fullPath, "utf-8");
    } catch (_e) {
      return ""; // File doesn't exist or unreadable
    }
  }

  private extractHuman(userMd: string): Identity["human"] {
    // Parse USER.md for:
    // - **Name:** Neto Pompeu
    // - **Timezone:** America/Cayenne
    const nameMatch = userMd.match(/\*\*Name:\*\*\s*(.+)/i);
    const timezoneMatch = userMd.match(/\*\*Timezone:\*\*\s*(.+)/i);
    const locationMatch = userMd.match(/\*\*Notes:\*\*\s*(.+Guyane française)/i);

    return {
      name: nameMatch?.[1]?.trim() || "Neto",
      role: "Dirigeant Primo Studio",
      location: locationMatch ? "Guyane française" : "Unknown",
      timezone: timezoneMatch?.[1]?.trim() || "America/Cayenne",
    };
  }

  private extractProjects(companyMd: string, objectivesMd: string): Identity["activeProjects"] {
    // Hardcoded for now — can be improved with regex parsing later
    // Based on USER.md "Façon de penser & Motivations"
    return {
      "Bureau": { weight: 0.9, status: "daily", type: "product" },
      "Polymarket": { weight: 0.8, status: "daily", type: "revenue" },
      "Primask": { weight: 0.6, status: "paused", type: "product" },
      "DockGroups": { weight: 0.3, status: "backlog", type: "product" },
      "Memoria": { weight: 0.5, status: "active", type: "internal_tool" },
      "Transport Rino": { weight: 0.4, status: "paused", type: "product" },
    };
  }

  private extractPreferences(userMd: string): string[] {
    // Extract from "## Personnalité & Communication" section
    // Look for bullet points and list items
    const preferences: string[] = [];
    
    const lines = userMd.split("\n");
    let inPreferences = false;
    
    for (const line of lines) {
      if (line.includes("Personnalité & Communication")) {
        inPreferences = true;
        continue;
      }
      if (inPreferences && line.startsWith("##")) {
        break; // End of section
      }
      if (inPreferences && (line.trim().startsWith("-") || line.trim().startsWith("*"))) {
        const pref = line.replace(/^[\s\-\*]+/, "").trim();
        if (pref.length > 10) preferences.push(pref);
      }
    }

    return preferences;
  }

  private extractTriggers(userMd: string): Identity["triggers"] {
    // Extract trigger words from USER.md
    return {
      frustration: ["putain", "ça marche pas", "encore", "crash", "bug"],
      satisfaction: ["nickel", "parfait", "super", "excellent", "top"],
      urgency: ["urgent", "maintenant", "vite", "asap", "rapidement"],
    };
  }
}
