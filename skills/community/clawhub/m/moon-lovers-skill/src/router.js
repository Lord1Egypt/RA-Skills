"use strict";

const ROUTES = {
  comfort: {
    description: "Receive distress first, then offer specific care.",
    outputMode: "reply",
    length: "medium",
  },
  light_teasing: {
    description: "Keep the mood light, playful, and face-saving.",
    outputMode: "reply",
    length: "short",
  },
  quiet_affection: {
    description: "Mirror warmth and imply specialness without over-confirming.",
    outputMode: "reply",
    length: "medium",
  },
  low_pressure_invitation: {
    description: "Move the interaction forward with an easy opt-out.",
    outputMode: "reply",
    length: "medium",
  },
  boundary_deescalation: {
    description: "Reduce heat while preserving dignity and connection.",
    outputMode: "reply",
    length: "short",
  },
  white_moonlight_reflection: {
    description: "Handle regret, distance, projection, and unforgettable afterglow.",
    outputMode: "reply",
    length: "medium",
  },
  analysis: {
    description: "Explain emotional reading, strategy, and a sendable draft.",
    outputMode: "analysis",
    length: "medium",
  },
  topic_continuation: {
    description: "Keep the conversation flowing when no stronger signal dominates.",
    outputMode: "reply",
    length: "short",
  },
};

const RULES = [
  {
    route: "analysis",
    weight: 10,
    patterns: [/分析/, /拆解/, /判断/, /策略/, /为什么/, /怎么回/, /帮我分析/, /给我思路/],
  },
  {
    route: "comfort",
    weight: 8,
    patterns: [
      /累/,
      /困/,
      /难受/,
      /不舒服/,
      /头疼/,
      /发烧/,
      /烦/,
      /焦虑/,
      /委屈/,
      /失望/,
      /崩溃/,
      /心情不好/,
      /不想说话/,
      /压力/,
    ],
  },
  {
    route: "boundary_deescalation",
    weight: 8,
    patterns: [/别这样/, /冷静/, /算了/, /先这样/, /越界/, /太快/, /别逼/, /压力太大/, /不合适/, /别当真/],
  },
  {
    route: "low_pressure_invitation",
    weight: 7,
    patterns: [/要不要/, /一起/, /见面/, /出来/, /喝咖啡/, /吃饭/, /下次/, /改天/, /有空/, /周末/],
  },
  {
    route: "light_teasing",
    weight: 6,
    patterns: [/怎么每次/, /你又/, /嘴硬/, /这么快/, /偷偷/, /是不是故意/, /被我抓到/, /逗我/],
  },
  {
    route: "quiet_affection",
    weight: 6,
    patterns: [/想你/, /想见你/, /在意/, /记得/, /偏心/, /特别/, /舍不得/, /好像有点喜欢/, /会想起你/],
  },
];

const WHITE_MOONLIGHT_SIGNALS = [
  { tag: "idealized", patterns: [/完美/, /几乎没有缺点/, /特别美好/, /像光/] },
  { tag: "incomplete", patterns: [/如果当时/, /没来得及/, /后来没有/, /错过/] },
  { tag: "limited_contact", patterns: [/没见几次/, /接触不多/, /不算熟/, /了解不多/] },
  { tag: "high_trigger", patterns: [/一直想起/, /反复想起/, /忘不掉/, /总会想起/, /总想起/, /经常想起/] },
  { tag: "unattainable", patterns: [/得不到/, /不能拥有/, /不是我的/, /不可能在一起/] },
  { tag: "trigger_scene", patterns: [/夜里/, /深夜/, /音乐/, /喝酒/, /下雨/, /某个场景/] },
  { tag: "fantasy_led", patterns: [/脑补/, /想象出来/, /其实并不了解/, /投射/] },
];

function scoreRoute(text) {
  const scores = Object.fromEntries(Object.keys(ROUTES).map((key) => [key, 0]));

  for (const rule of RULES) {
    for (const pattern of rule.patterns) {
      if (pattern.test(text)) {
        scores[rule.route] += rule.weight;
      }
    }
  }

  if (scores.analysis > 0) {
    scores.topic_continuation -= 1;
  }

  return scores;
}

function detectWhiteMoonlightSignals(text) {
  return WHITE_MOONLIGHT_SIGNALS
    .filter((signal) => signal.patterns.some((pattern) => pattern.test(text)))
    .map((signal) => signal.tag);
}

function inferRelationshipStage(text) {
  if (/在一起|恋爱|对象|男朋友|女朋友|复合/.test(text)) {
    return "established_or_post_confession";
  }

  if (/刚认识|暧昧|试探|还没确认|还不熟/.test(text)) {
    return "ambiguous_early_stage";
  }

  return "unspecified";
}

function inferIntensity(text) {
  if (/很|特别|非常|一直|反复|忘不掉|崩溃|太|总会|经常/.test(text)) {
    return "high";
  }

  if (/有点|还行|偶尔/.test(text)) {
    return "low";
  }

  return "medium";
}

function selectPrimaryRoute(scores) {
  const ranked = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const [route, score] = ranked[0];

  if (score <= 0) {
    return {
      primaryRoute: "topic_continuation",
      secondaryRoutes: [],
    };
  }

  const secondaryRoutes = ranked
    .slice(1)
    .filter(([, value]) => value > 0)
    .slice(0, 2)
    .map(([key]) => key);

  return {
    primaryRoute: route,
    secondaryRoutes,
  };
}

function routeInput(input) {
  const text = String(input || "").trim();
  const scores = scoreRoute(text);
  const whiteMoonlightSignals = detectWhiteMoonlightSignals(text);
  const relationshipStage = inferRelationshipStage(text);
  const intensity = inferIntensity(text);
  const whiteMoonlightWeighted =
    whiteMoonlightSignals.length >= 2 ||
    (whiteMoonlightSignals.includes("incomplete") && whiteMoonlightSignals.includes("high_trigger")) ||
    (whiteMoonlightSignals.includes("limited_contact") && whiteMoonlightSignals.includes("trigger_scene")) ||
    (whiteMoonlightSignals.includes("unattainable") && whiteMoonlightSignals.includes("trigger_scene"));

  if (whiteMoonlightWeighted) {
    scores.white_moonlight_reflection += 9;
  }

  const { primaryRoute, secondaryRoutes } = selectPrimaryRoute(scores);

  return {
    input: text,
    primaryRoute,
    secondaryRoutes,
    routeConfig: ROUTES[primaryRoute],
    relationshipStage,
    intensity,
    whiteMoonlightSignals,
    shouldUseWhiteMoonlightTone: whiteMoonlightSignals.length > 0,
    scores,
  };
}

function readCliInput() {
  const args = process.argv.slice(2).join(" ").trim();

  if (args) {
    return Promise.resolve(args);
  }

  return new Promise((resolve) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data.trim()));
  });
}

async function main() {
  const input = await readCliInput();

  if (!input) {
    console.error("Usage: npm run route -- <text>");
    process.exitCode = 1;
    return;
  }

  const result = routeInput(input);
  console.log(JSON.stringify(result, null, 2));
}

if (require.main === module) {
  main();
}

module.exports = {
  ROUTES,
  RULES,
  WHITE_MOONLIGHT_SIGNALS,
  routeInput,
};
