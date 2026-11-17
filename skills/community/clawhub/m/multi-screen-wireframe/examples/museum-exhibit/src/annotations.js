(function defineMuseumAnnotations({ defineAnnotations }) {
  defineAnnotations({
    annotationsRevision: 'museum-r1',
    annotations: [
      {
        id: 'ann-home-featured',
        screenId: 'home',
        screenTitle: '首页',
        anchor: {
          kind: 'node',
          selector: '#home-featured',
          fallbackPosition: { x: 0.5, y: 0.32 },
        },
        content: '首页特展卡片应突出当前主推专题，点击进入专题详情。',
        status: 'open',
        createdAt: '2026-08-11T06:00:00.000Z',
        updatedAt: '2026-08-11T06:00:00.000Z',
      },
      {
        id: 'ann-artifact-audio',
        screenId: 'artifact-detail',
        screenTitle: '展品详情',
        anchor: {
          kind: 'node',
          selector: '#artifact-detail-audio-toggle',
          fallbackPosition: { x: 0.82, y: 0.42 },
        },
        content: '语音导览开关控制屏内讲解状态，实际产品需对接音频播放与进度。',
        status: 'open',
        createdAt: '2026-08-11T06:00:00.000Z',
        updatedAt: '2026-08-11T06:00:00.000Z',
      },
      {
        id: 'ann-floor-map',
        screenId: 'floor-map',
        screenTitle: '楼层导览',
        anchor: { kind: 'screen' },
        content: '地图标记需与展厅数据联动，点击 marker 跳转对应专题或展品。',
        status: 'open',
        createdAt: '2026-08-11T06:00:00.000Z',
        updatedAt: '2026-08-11T06:00:00.000Z',
      },
    ],
  })
})(window.WireframeVue)
