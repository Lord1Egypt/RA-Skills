const SHARED_ALIASES = {
  action: {
    on: ['つけて', 'つける', 'オン'],
    off: ['消して', 'けして', 'オフ', '止めて', 'とめて'],
    set_mode: ['にして', 'して'],
  },
};

const DOMAINS = {
  light: {
    intentPrefix: 'light',
    deviceAliases: ['電気', 'ライト', '照明'],
    actions: {
      on: ['つけて', 'つける', 'オン'],
      off: ['消して', 'けして', 'オフ'],
    },
    requiredSlotsByIntent: {
      light_on: ['device', 'action'],
      light_off: ['device', 'action'],
    },
  },
  aircon: {
    intentPrefix: 'aircon',
    deviceAliases: ['エアコン'],
    actions: {
      on: ['つけて'],
      off: ['消して', '止めて', 'とめて'],
      set_mode: ['にして', 'つけて', 'して'],
    },
    modes: {
      cool: ['冷房', 'れいぼう', 'れーぼー', 'れいほう', '涼しくして'],
      heat: ['暖房', 'だんぼう', 'だんぼー', '暖かくして'],
      dry: ['除湿', 'じょしつ', '除しつ'],
      fan: ['送風', 'そうふう', '風だけ'],
    },
    requiredSlotsByIntent: {
      aircon_on: ['device', 'action'],
      aircon_off: ['device', 'action'],
      aircon_mode_cool: ['device', 'action', 'mode'],
      aircon_mode_heat: ['device', 'action', 'mode'],
      aircon_mode_dry: ['device', 'action', 'mode'],
      aircon_mode_fan: ['device', 'action', 'mode'],
    },
  },
  curtain: {
    intentPrefix: 'curtain',
    deviceAliases: ['カーテン', 'ブラインド'],
    actions: {
      open: ['開けて', 'あけて'],
      close: ['閉めて', 'しめて'],
    },
    requiredSlotsByIntent: {
      curtain_open: ['device', 'action'],
      curtain_close: ['device', 'action'],
    },
  },
  tv: {
    intentPrefix: 'tv',
    deviceAliases: ['テレビ', 'TV'],
    actions: {
      on: ['つけて'],
      off: ['消して'],
    },
    requiredSlotsByIntent: {
      tv_on: ['device', 'action'],
      tv_off: ['device', 'action'],
    },
  },
};

function buildProfile(domains = DOMAINS) {
  const devices = Object.fromEntries(
    Object.entries(domains).map(([domainName, domain]) => [domainName, domain.deviceAliases || []]),
  );

  const actions = Object.entries(domains).reduce((acc, [, domain]) => {
    for (const [actionName, aliases] of Object.entries(domain.actions || {})) {
      acc[actionName] = Array.from(new Set([...(acc[actionName] || []), ...aliases, ...(SHARED_ALIASES.action[actionName] || [])]));
    }
    return acc;
  }, {});

  const modes = Object.entries(domains).reduce((acc, [, domain]) => {
    for (const [modeName, aliases] of Object.entries(domain.modes || {})) {
      acc[modeName] = Array.from(new Set([...(acc[modeName] || []), ...aliases]));
    }
    return acc;
  }, {});

  return { domains, devices, actions, modes };
}

const DEFAULT_PROFILE = buildProfile();

export { DOMAINS, SHARED_ALIASES, buildProfile, DEFAULT_PROFILE };
