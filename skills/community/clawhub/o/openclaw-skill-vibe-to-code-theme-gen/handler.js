const SYSTEM_INSTRUCTION = `You are a professional UI designer. Translate the user's vibe into a JSON object containing: 1. primaryColor, 2. secondaryColor, 3. accentColor, 4. backgroundColor, and 5. fontStack (e.g., Serif or Sans-Serif). Respond ONLY with valid JSON.`;

// --- Formatters ---

function toCSS(theme) {
  const vars = Object.entries({
    '--primary-color': theme.primaryColor,
    '--secondary-color': theme.secondaryColor,
    '--accent-color': theme.accentColor,
    '--background-color': theme.backgroundColor,
    '--font-stack': theme.fontStack,
  })
    .map(([k, v]) => `  ${k}: ${v};`)
    .join('\n');

  return `:root {\n${vars}\n}`;
}

function toTailwind(theme) {
  return JSON.stringify(
    {
      colors: {
        primary: theme.primaryColor,
        secondary: theme.secondaryColor,
        accent: theme.accentColor,
        background: theme.backgroundColor,
      },
      fontFamily: {
        vibe: theme.fontStack,
      },
    },
    null,
    2
  );
}

function toVSCode(theme) {
  return JSON.stringify(
    {
      'workbench.colorCustomizations': {
        'editor.background': theme.backgroundColor,
        'editor.foreground': theme.primaryColor,
        'editorLineNumber.foreground': theme.secondaryColor,
        'editorCursor.foreground': theme.accentColor,
        'activityBar.background': theme.backgroundColor,
        'sideBar.background': theme.backgroundColor,
        'editor.fontFamily': theme.fontStack,
      },
    },
    null,
    2
  );
}

const FORMATTERS = {
  css: toCSS,
  tailwind: toTailwind,
  vscode: toVSCode,
};

// --- Main ---

async function generateTheme(vibe, format = 'css') {
  const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      model: 'openai/gpt-oss-120b',
      messages: [
        { role: 'system', content: SYSTEM_INSTRUCTION },
        { role: 'user', content: vibe },
      ],
    }),
  });

  const data = await response.json();
  const text = data.choices?.[0]?.message?.content ?? '';
  const theme = JSON.parse(text);

  const formatter = FORMATTERS[format] ?? FORMATTERS.css;
  return formatter(theme);
}

module.exports = { generateTheme, toCSS, toTailwind, toVSCode };
