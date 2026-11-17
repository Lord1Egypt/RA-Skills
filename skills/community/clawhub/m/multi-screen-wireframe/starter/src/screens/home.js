/**
 * @wireframe-skill multi-screen-wireframe@2.1.0
 * 创建基于 v2.0.0
 * 修改基于 v2.1.0
 */
WireframeVue.defineScreen('home', () => ({
  template: /*html*/ `
    <WfColumn
      id="home-page"
      class="home-page"
      :gap="16"
      :style="{ padding: '24px' }"
    >
      <WfHeading id="home-title" class="home-page__title" :level="1">
        线框首页
      </WfHeading>
      <WfText class="home-page__description">
        从 src/screens 开始编辑页面，保存后刷新浏览器即可。
      </WfText>
      <WfButton id="home-detail-action" class="home-page__detail-action" to="detail">
        查看详情
      </WfButton>
    </WfColumn>
  `,
}))
