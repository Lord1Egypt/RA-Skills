#!/usr/bin/env node

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

// ─── BVI Anchorage Database ───────────────────────────────────────────

interface Anchorage {
  name: string;
  island: string;
  lat: number;
  lon: number;
  mooringBalls: boolean;
  nationalPark: boolean;
  parkFee?: number;
  difficulty: "easy" | "moderate" | "advanced";
  highlights: string[];
  provisions: boolean;
  fuel: boolean;
  restaurants: boolean;
  customs: boolean;
  description: string;
}

const ANCHORAGES: Anchorage[] = [
  {
    name: "The Baths",
    island: "Virgin Gorda",
    lat: 18.4286,
    lon: -64.4428,
    mooringBalls: true,
    nationalPark: true,
    parkFee: 5,
    difficulty: "moderate",
    highlights: ["Giant granite boulders", "Snorkeling grottos", "Iconic photo spot"],
    provisions: false,
    fuel: false,
    restaurants: true,
    customs: false,
    description: "Iconic BVI destination with cathedral-like granite boulder formations. Day moorings only — no overnight stays. Arrive early to secure a mooring ball.",
  },
  {
    name: "The Bight",
    island: "Norman Island",
    lat: 18.3178,
    lon: -64.6186,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "easy",
    highlights: ["Pirates Bight restaurant", "Willy T floating bar", "Snorkeling at The Caves"],
    provisions: false,
    fuel: false,
    restaurants: true,
    customs: false,
    description: "Said to be the inspiration for Treasure Island. Great overnight anchorage with restaurant, floating bar, and nearby caves for snorkeling.",
  },
  {
    name: "Great Harbour",
    island: "Jost Van Dyke",
    lat: 18.4428,
    lon: -64.7531,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "easy",
    highlights: ["Foxy's Bar", "New Year's Eve party", "Beach bars"],
    provisions: true,
    fuel: false,
    restaurants: true,
    customs: true,
    description: "Home of the legendary Foxy's Bar. Check in at customs here when arriving from USVI. Lively beach bar scene.",
  },
  {
    name: "White Bay",
    island: "Jost Van Dyke",
    lat: 18.4389,
    lon: -64.7636,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "moderate",
    highlights: ["Soggy Dollar Bar", "Painkiller cocktail birthplace", "White sand beach"],
    provisions: false,
    fuel: false,
    restaurants: true,
    customs: false,
    description: "Home of the Soggy Dollar Bar and the original Painkiller cocktail. Beautiful white sand beach. Can be rolly in northerly swells.",
  },
  {
    name: "Setting Point",
    island: "Anegada",
    lat: 18.7269,
    lon: -64.3378,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "advanced",
    highlights: ["Lobster dinners", "Flamingo pond", "Pristine beaches", "Horseshoe Reef"],
    provisions: true,
    fuel: false,
    restaurants: true,
    customs: true,
    description: "Low-lying coral island with the largest barrier reef in the Caribbean. Navigation requires careful attention to coral heads. Famous for lobster dinners at Anegada Reef Hotel.",
  },
  {
    name: "Cooper Island Beach Club",
    island: "Cooper Island",
    lat: 18.3872,
    lon: -64.5131,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "easy",
    highlights: ["Eco-resort", "Craft microbrewery", "Rum bar", "Good snorkeling"],
    provisions: false,
    fuel: false,
    restaurants: true,
    customs: false,
    description: "Eco-friendly beach club with a microbrewery and rum bar. Excellent snorkeling right off the mooring field. Solar-powered resort.",
  },
  {
    name: "Cane Garden Bay",
    island: "Tortola",
    lat: 18.4322,
    lon: -64.6611,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "easy",
    highlights: ["Beach bars", "Live music", "Callwood Rum Distillery", "Swimming beach"],
    provisions: true,
    fuel: false,
    restaurants: true,
    customs: false,
    description: "Popular bay on Tortola's north shore with beach bars, live music, and the historic Callwood Rum Distillery. Can be rolly in northerly swells.",
  },
  {
    name: "Soper's Hole",
    island: "Tortola",
    lat: 18.3897,
    lon: -64.7003,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "easy",
    highlights: ["Shopping", "Provisioning", "Restaurants", "Protected harbor"],
    provisions: true,
    fuel: true,
    restaurants: true,
    customs: true,
    description: "Well-protected harbor at the west end of Tortola. Good provisioning, fuel dock, and customs clearance. Popular starting/ending point for charters.",
  },
  {
    name: "Road Town",
    island: "Tortola",
    lat: 18.4264,
    lon: -64.6208,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "easy",
    highlights: ["Capital city", "Provisioning", "Marina facilities"],
    provisions: true,
    fuel: true,
    restaurants: true,
    customs: true,
    description: "BVI capital and main port of entry. Full marina facilities, provisioning, and customs. Most charter companies are based here.",
  },
  {
    name: "Manchioneel Bay",
    island: "Cooper Island",
    lat: 18.3856,
    lon: -64.5097,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "easy",
    highlights: ["Quiet anchorage", "Snorkeling", "Hiking trails"],
    provisions: false,
    fuel: false,
    restaurants: false,
    customs: false,
    description: "Quiet alternative to the main Cooper Island Beach Club mooring field. Good snorkeling and hiking.",
  },
  {
    name: "The Dogs",
    island: "The Dogs",
    lat: 18.4667,
    lon: -64.5000,
    mooringBalls: true,
    nationalPark: true,
    parkFee: 5,
    difficulty: "moderate",
    highlights: ["World-class diving", "Snorkeling walls", "Uninhabited islands"],
    provisions: false,
    fuel: false,
    restaurants: false,
    customs: false,
    description: "Group of uninhabited islands between Virgin Gorda and Tortola. Excellent diving and snorkeling with dramatic underwater walls.",
  },
  {
    name: "Spanish Town",
    island: "Virgin Gorda",
    lat: 18.4478,
    lon: -64.4308,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "easy",
    highlights: ["Virgin Gorda Yacht Harbour", "Provisioning", "Restaurants"],
    provisions: true,
    fuel: true,
    restaurants: true,
    customs: true,
    description: "Main settlement on Virgin Gorda with full marina services. Good spot for provisioning and customs clearance.",
  },
  {
    name: "North Sound",
    island: "Virgin Gorda",
    lat: 18.4914,
    lon: -64.3881,
    mooringBalls: true,
    nationalPark: false,
    difficulty: "moderate",
    highlights: ["Bitter End Yacht Club", "Saba Rock", "Kiteboarding", "Protected waters"],
    provisions: true,
    fuel: true,
    restaurants: true,
    customs: false,
    description: "Large protected sound on the northeast of Virgin Gorda. Home to the Bitter End Yacht Club and Saba Rock resort. Excellent for watersports.",
  },
  {
    name: "Sandy Spit",
    island: "Sandy Spit",
    lat: 18.4500,
    lon: -64.7167,
    mooringBalls: false,
    nationalPark: false,
    difficulty: "moderate",
    highlights: ["Tiny desert island", "Photo opportunity", "Snorkeling"],
    provisions: false,
    fuel: false,
    restaurants: false,
    customs: false,
    description: "Tiny uninhabited sand cay near Jost Van Dyke. Classic Caribbean desert island look. Day stop only — no overnight anchoring.",
  },
];

// ─── Season & Weather Logic ──────────────────────────────────────────

interface SeasonInfo {
  season: string;
  tradeWinds: string;
  swellRisk: string;
  hurricaneRisk: string;
  temperature: string;
  notes: string;
}

function getSeasonInfo(startDate: Date): SeasonInfo {
  const month = startDate.getMonth(); // 0-indexed

  if (month >= 11 || month <= 3) {
    // Dec–Apr: High season
    return {
      season: "High Season (Winter)",
      tradeWinds: "15–25 knots from the east/northeast. Christmas winds can gust to 30+ knots in December–January.",
      swellRisk: "Moderate northerly swells possible. Bays on the north side (Cane Garden Bay, White Bay) can be uncomfortable.",
      hurricaneRisk: "None",
      temperature: "75–85°F (24–29°C) air, 78–80°F (26–27°C) water",
      notes: "Peak charter season. Moorings and anchorages fill early. Book restaurants in advance. Christmas winds in Dec–Jan can make passages choppy.",
    };
  } else if (month >= 4 && month <= 5) {
    // May–Jun: Shoulder
    return {
      season: "Shoulder Season (Late Spring)",
      tradeWinds: "10–18 knots, lighter and more variable than winter. Occasional calms.",
      swellRisk: "Low. Seas generally calmer.",
      hurricaneRisk: "Very low but early tropical activity possible in June.",
      temperature: "80–88°F (27–31°C) air, 80–82°F (27–28°C) water",
      notes: "Excellent sailing conditions with lighter winds. Fewer crowds. Watch for early-season tropical disturbances in June.",
    };
  } else {
    // Jul–Nov: Hurricane season
    return {
      season: "Hurricane Season (Summer/Fall)",
      tradeWinds: "Variable, 8–20 knots. Periods of light air common.",
      swellRisk: "Elevated. Tropical swells from the south/southeast possible.",
      hurricaneRisk: "HIGH — peak is August through October. Monitor NOAA forecasts daily.",
      temperature: "82–90°F (28–32°C) air, 82–84°F (28–29°C) water",
      notes: "CRITICAL: Monitor weather daily. Have a hurricane plan. Know where hurricane holes are (Paraquita Bay, Road Town). Insurance may not cover hurricane season charters. Fewer services open.",
    };
  }
}

// ─── Itinerary Generator ─────────────────────────────────────────────

interface ItineraryDay {
  day: number;
  date: string;
  location: string;
  island: string;
  activities: string[];
  sailing: string;
  notes: string;
}

function daysBetween(start: Date, end: Date): number {
  return Math.ceil((end.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
}

function formatDate(date: Date): string {
  return date.toISOString().split("T")[0];
}

function generateItinerary(
  startDate: Date,
  endDate: Date,
  experience: "beginner" | "intermediate" | "expert",
  interests: string[]
): ItineraryDay[] {
  const numDays = daysBetween(startDate, endDate);

  // Define route templates based on experience level
  const beginnerRoute = [
    "Road Town",
    "The Bight",
    "Cooper Island Beach Club",
    "Spanish Town",
    "The Baths",
    "Cane Garden Bay",
    "Soper's Hole",
    "Road Town",
  ];

  const intermediateRoute = [
    "Road Town",
    "The Dogs",
    "North Sound",
    "The Baths",
    "Cooper Island Beach Club",
    "The Bight",
    "Great Harbour",
    "White Bay",
    "Sandy Spit",
    "Cane Garden Bay",
    "Soper's Hole",
    "Road Town",
  ];

  const expertRoute = [
    "Road Town",
    "The Dogs",
    "North Sound",
    "Setting Point",
    "Setting Point",
    "The Baths",
    "Cooper Island Beach Club",
    "The Bight",
    "Great Harbour",
    "White Bay",
    "Sandy Spit",
    "Manchioneel Bay",
    "Cane Garden Bay",
    "Soper's Hole",
    "Road Town",
  ];

  const routeMap: Record<string, string[]> = {
    beginner: beginnerRoute,
    intermediate: intermediateRoute,
    expert: expertRoute,
  };

  const route = routeMap[experience];

  // Fit route to available days
  const stopsNeeded = numDays + 1; // including start
  let selectedStops: string[];

  if (stopsNeeded >= route.length) {
    selectedStops = route;
  } else {
    // Sample evenly from the route
    selectedStops = [route[0]];
    const step = (route.length - 1) / (stopsNeeded - 1);
    for (let i = 1; i < stopsNeeded - 1; i++) {
      selectedStops.push(route[Math.round(i * step)]);
    }
    selectedStops.push(route[route.length - 1]);
  }

  const itinerary: ItineraryDay[] = [];
  const hasInterest = (keyword: string) =>
    interests.some((i) => i.toLowerCase().includes(keyword));

  for (let day = 0; day < numDays; day++) {
    const currentDate = new Date(startDate);
    currentDate.setDate(currentDate.getDate() + day);
    const stopName = selectedStops[Math.min(day, selectedStops.length - 1)];
    const anchorage = ANCHORAGES.find((a) => a.name === stopName);

    const activities: string[] = [];
    let sailing = "";
    let notes = "";

    if (day === 0) {
      activities.push("Pick up charter vessel, safety briefing, stow provisions");
      if (anchorage?.customs) {
        activities.push("Clear customs if needed");
      }
      sailing = "Short afternoon sail to first anchorage (2–4 nm)";
      notes = "Depart by early afternoon to reach first anchorage before sunset.";
    } else if (day === numDays - 1) {
      sailing = "Final sail back to base (varies)";
      notes = "Return vessel by check-in time. Allow time for customs clearance if needed. Top off fuel and water.";
      activities.push("Return to charter base");
      activities.push("Vessel check-out");
    } else {
      if (anchorage) {
        activities.push(...anchorage.highlights);
        if (anchorage.nationalPark) {
          notes += `National park fee: $${anchorage.parkFee}/person. `;
        }
        if (anchorage.mooringBalls) {
          notes += "Mooring balls available ($25–35/night). ";
        }
        if (anchorage.restaurants) {
          activities.push("Dinner ashore");
        }

        // Add interest-based activities
        if (hasInterest("snorkel") || hasInterest("dive")) {
          activities.push("Snorkeling/diving at nearby reef");
        }
        if (hasInterest("fish")) {
          activities.push("Trolling line out during passage");
        }
        if (hasInterest("photo")) {
          activities.push("Sunrise/sunset photography");
        }
        if (hasInterest("history") || hasInterest("culture")) {
          activities.push("Explore local history and culture");
        }

        sailing = `Morning sail to ${anchorage.name} (${anchorage.island})`;
      } else {
        sailing = `Sail to ${stopName}`;
      }
    }

    itinerary.push({
      day: day + 1,
      date: formatDate(currentDate),
      location: stopName,
      island: anchorage?.island || stopName,
      activities,
      sailing,
      notes: notes.trim(),
    });
  }

  return itinerary;
}

// ─── Provisioning Generator ──────────────────────────────────────────

interface ProvisionItem {
  category: string;
  item: string;
  quantity: string;
  notes: string;
}

function generateProvisioning(guests: number, numDays: number): ProvisionItem[] {
  const items: ProvisionItem[] = [];
  const mealsPerDay = 3;
  const totalMeals = numDays * mealsPerDay;
  const dineOutMeals = Math.floor(numDays * 0.4) * guests; // ~40% meals ashore

  // Water — 1 gallon per person per day for drinking/cooking
  items.push({
    category: "Beverages",
    item: "Drinking water",
    quantity: `${guests * numDays} gallons`,
    notes: "1 gallon per person per day minimum. More in summer heat.",
  });

  items.push({
    category: "Beverages",
    item: "Ice",
    quantity: `${Math.ceil(guests * numDays * 0.5)} bags`,
    notes: "Restock at marinas. Ice is precious on a boat!",
  });

  items.push({
    category: "Beverages",
    item: "Beer/drinks",
    quantity: `${guests * numDays * 2} cans/bottles`,
    notes: "Adjust to preference. Keep cans to reduce breakage risk.",
  });

  items.push({
    category: "Beverages",
    item: "Rum",
    quantity: `${Math.ceil(guests / 2)} bottles`,
    notes: "It's the BVI — Pusser's Rum for Painkillers is a must.",
  });

  items.push({
    category: "Beverages",
    item: "Coffee/Tea",
    quantity: `${Math.ceil(guests * numDays * 0.5)} servings`,
    notes: "Bring a French press — works great on boats.",
  });

  // Proteins
  const proteinServings = guests * numDays;
  items.push({
    category: "Proteins",
    item: "Chicken breasts/thighs",
    quantity: `${Math.ceil(proteinServings * 0.3)} lbs`,
    notes: "Freeze half and use later in the trip.",
  });

  items.push({
    category: "Proteins",
    item: "Fresh fish",
    quantity: "Buy local when available",
    notes: "Buy from local fishermen at anchorages. Mahi, wahoo, and snapper are common.",
  });

  items.push({
    category: "Proteins",
    item: "Eggs",
    quantity: `${Math.ceil(guests * numDays * 0.5)} count`,
    notes: "Great for quick breakfasts. Store carefully.",
  });

  items.push({
    category: "Proteins",
    item: "Deli meats & cheese",
    quantity: `${Math.ceil(guests * 0.3)} lbs`,
    notes: "For sandwiches during day sails.",
  });

  // Produce
  items.push({
    category: "Produce",
    item: "Limes & lemons",
    quantity: `${guests * numDays} count`,
    notes: "Essential for drinks and cooking. Limes last well on a boat.",
  });

  items.push({
    category: "Produce",
    item: "Tomatoes, lettuce, onions",
    quantity: `${Math.ceil(guests * numDays * 0.3)} lbs each`,
    notes: "Use delicate produce first. Onions and tomatoes last longer.",
  });

  items.push({
    category: "Produce",
    item: "Tropical fruit",
    quantity: `${guests * numDays} pieces`,
    notes: "Bananas, mangoes, papayas — buy at local markets when possible.",
  });

  // Staples
  items.push({
    category: "Staples",
    item: "Bread/wraps",
    quantity: `${Math.ceil(guests * numDays * 0.3)} loaves/packs`,
    notes: "Wraps last longer than bread in tropical heat.",
  });

  items.push({
    category: "Staples",
    item: "Pasta & rice",
    quantity: `${Math.ceil(guests * numDays * 0.1)} lbs`,
    notes: "Easy one-pot meals aboard.",
  });

  items.push({
    category: "Staples",
    item: "Chips & snacks",
    quantity: `${Math.ceil(guests * numDays * 0.2)} bags`,
    notes: "Sailing makes people snacky.",
  });

  items.push({
    category: "Staples",
    item: "Condiments & spices",
    quantity: "1 set",
    notes: "Salt, pepper, hot sauce, olive oil, garlic, soy sauce minimum.",
  });

  // Safety & Comfort
  items.push({
    category: "Safety & Comfort",
    item: "Reef-safe sunscreen",
    quantity: `${Math.ceil(guests * 1.5)} bottles`,
    notes: "REEF-SAFE ONLY. BVI protects its reefs. Reapply frequently.",
  });

  items.push({
    category: "Safety & Comfort",
    item: "Dramamine/seasickness meds",
    quantity: `${guests} packs`,
    notes: "Have aboard even if no one expects to need it.",
  });

  items.push({
    category: "Safety & Comfort",
    item: "Bug spray",
    quantity: `${Math.ceil(guests / 2)} bottles`,
    notes: "No-see-ums at anchorages at dusk. Essential.",
  });

  items.push({
    category: "Safety & Comfort",
    item: "First aid kit supplements",
    quantity: "1 kit",
    notes: "Ibuprofen, antihistamines, bandages, antiseptic. Charter boat has basic kit.",
  });

  return items;
}

// ─── Tips Generator ──────────────────────────────────────────────────

function generateTips(
  experience: "beginner" | "intermediate" | "expert",
  numDays: number,
  season: SeasonInfo
): string[] {
  const tips: string[] = [];

  // Universal tips
  tips.push(
    "BVI customs: Clear in at Road Town, Jost Van Dyke, or Spanish Town. You need a cruising permit ($4/person/day). Have passports and boat documentation ready."
  );
  tips.push(
    "Mooring balls: Most BVI anchorages use mooring balls ($25–35/night). Pick up with a boat hook from the bow — never tie to the pickup line, use your own line through the pennant."
  );
  tips.push(
    "National park fees: The Baths, The Dogs, and other national parks charge $5/person. Have cash ready."
  );
  tips.push(
    "VHF Channel 16 for emergencies, Channel 12 for BVI port authority. Monitor weather on Channel 2 (WX)."
  );

  if (experience === "beginner") {
    tips.push(
      "Keep passages short (under 10 nm) for your first few days. The BVI is compact — no need to rush."
    );
    tips.push(
      "Practice picking up mooring balls before you need to in a crowded harbor. Assign crew roles: helm, bow, and line handler."
    );
    tips.push(
      "Motor into the wind/current when picking up a mooring ball. Approach slowly — you can always go around."
    );
    tips.push(
      "Reef the main before you think you need to. It's easier to shake out a reef than to put one in when overpowered."
    );
  }

  if (experience === "intermediate") {
    tips.push(
      "Consider a night sail from Anegada back to Virgin Gorda — the stars are incredible with no light pollution."
    );
    tips.push(
      "The passage to Anegada requires careful navigation around Horseshoe Reef. Use waypoints and follow the marked channel."
    );
  }

  if (experience === "expert") {
    tips.push(
      "For the Anegada passage, depart Virgin Gorda at first light. The reef approach is best with the sun high and behind you for reef reading."
    );
    tips.push(
      "Explore the less-visited south side of Norman Island — Benures Bay and Pelican Island have excellent diving."
    );
    tips.push(
      "The roundabout race course around Tortola makes for an excellent day of competitive sailing if your crew is up for it."
    );
  }

  if (numDays >= 7) {
    tips.push(
      "With a week or more, don't rush. Spend two nights at your favorite spots. The BVI rewards slow sailing."
    );
  }

  if (season.season.includes("Hurricane")) {
    tips.push(
      "CRITICAL: Check NOAA hurricane forecasts every morning and evening. Know the location of hurricane holes: Paraquita Bay (Tortola), North Sound (Virgin Gorda)."
    );
  }

  if (season.season.includes("Winter")) {
    tips.push(
      "Christmas winds (Dec–Jan) can blow 25+ knots. Reef early and avoid exposed north-facing bays during northerly swells."
    );
  }

  tips.push(
    "Provisioning tip: Rite Way and Bobby's Supermarket in Road Town are your best options. Prices are 2–3x US mainland — provision staples before arriving if possible."
  );

  tips.push(
    "Leave no trace: BVI waters are pristine because sailors respect them. No discharge, no trash overboard, use reef-safe sunscreen, don't touch coral."
  );

  return tips;
}

// ─── MCP Server Setup ────────────────────────────────────────────────

const server = new McpServer({
  name: "charter-planner",
  version: "1.0.0",
});

server.tool(
  "plan_charter",
  "Plan a BVI sailing charter with recommended itineraries, weather considerations, provisioning lists, and local tips. Covers real BVI anchorages including The Baths, Norman Island, Jost Van Dyke, Anegada, Cooper Island, and more.",
  {
    start_date: z.string().describe("Charter start date (YYYY-MM-DD format)"),
    end_date: z.string().describe("Charter end date (YYYY-MM-DD format)"),
    guests: z.number().min(1).max(20).describe("Number of guests aboard"),
    experience: z
      .enum(["beginner", "intermediate", "expert"])
      .describe("Sailing experience level of the crew"),
    interests: z
      .array(z.string())
      .optional()
      .describe("Optional interests: snorkeling, diving, fishing, photography, history, cuisine, nightlife"),
  },
  async ({ start_date, end_date, guests, experience, interests }) => {
    try {
      const startDate = new Date(start_date);
      const endDate = new Date(end_date);

      if (isNaN(startDate.getTime()) || isNaN(endDate.getTime())) {
        throw new Error("Invalid date format. Use YYYY-MM-DD.");
      }

      if (endDate <= startDate) {
        throw new Error("end_date must be after start_date.");
      }

      const numDays = daysBetween(startDate, endDate);
      if (numDays < 2) {
        throw new Error("Charter must be at least 2 days.");
      }
      if (numDays > 21) {
        throw new Error("Maximum charter planning is 21 days.");
      }

      const seasonInfo = getSeasonInfo(startDate);
      const itinerary = generateItinerary(
        startDate,
        endDate,
        experience,
        interests || []
      );
      const provisioning = generateProvisioning(guests, numDays);
      const tips = generateTips(experience, numDays, seasonInfo);

      const weatherNotes = [
        `Season: ${seasonInfo.season}`,
        `Trade Winds: ${seasonInfo.tradeWinds}`,
        `Swell Risk: ${seasonInfo.swellRisk}`,
        `Hurricane Risk: ${seasonInfo.hurricaneRisk}`,
        `Temperature: ${seasonInfo.temperature}`,
        `Notes: ${seasonInfo.notes}`,
      ].join("\n");

      const result = {
        itinerary,
        weather_notes: weatherNotes,
        provisioning,
        tips,
      };

      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      return {
        content: [
          {
            type: "text" as const,
            text: JSON.stringify({ error: `Charter planning failed: ${message}` }),
          },
        ],
        isError: true,
      };
    }
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
