/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('home', () => ({
  setup() {
    return {
      exhibitions: [
        { id: 'ex-bronze', title: '青铜时代', hall: '一层东厅', period: '商周 · 128 件', note: '礼器、兵器与祭祀用具' },
        { id: 'ex-porcelain', title: '瓷韵千年', hall: '二层南厅', period: '唐宋至清 · 96 件', note: '官窑、民窑与出口瓷器' },
        { id: 'ex-calligraphy', title: '翰墨风流', hall: '三层西厅', period: '魏晋至近代 · 74 件', note: '手卷、册页与碑拓' },
        { id: 'ex-silk', title: '丝路遗珍', hall: '一层西厅', period: '汉唐 · 52 件', note: '织锦、壁画与贸易器物' },
        { id: 'ex-jade', title: '玉润华章', hall: '二层北厅', period: '新石器至清 · 88 件', note: '佩饰、礼器与葬玉' },
      ],
      highlights: [
        { id: 'art-ding', title: '兽面纹青铜鼎', era: '商代晚期', hall: '一层东厅 03 号柜' },
        { id: 'art-vase', title: '青花缠枝莲瓶', era: '明永乐', hall: '二层南厅 12 号柜' },
        { id: 'art-scroll', title: '行书《快雪时晴》摹本', era: '清代', hall: '三层西厅 05 号柜' },
        { id: 'art-jade', title: '和田白玉璧', era: '汉代', hall: '二层北厅 08 号柜' },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="home-page" class="museum-page home__page" :gap="18">
        <WfPageHeader
          id="home-header"
          title-id="home-title"
          subtitle-id="home-subtitle"
          class="home__header"
          title="城市历史博物馆"
          subtitle="今日开放 09:00–17:30 · 建议预约时段入场"
        >
          <template #actions>
            <WfButton id="home-search-action" class="home__search-action" to="search">搜索</WfButton>
          </template>
        </WfPageHeader>

        <WfCard id="home-featured" class="museum-card home__featured" to="exhibition-detail">
          <WfImagePlaceholder class="home__featured-image" :height="188" :border-radius="0" />
          <WfColumn class="museum-card__body home__featured-body" :gap="10">
            <WfRow class="museum-chip-row home__featured-badges" :gap="8">
              <WfBadge class="home__featured-badge">特展</WfBadge>
              <WfBadge class="home__featured-badge">本月推荐</WfBadge>
            </WfRow>
            <WfHeading id="home-featured-title" class="home__featured-title" :level="2">青铜时代</WfHeading>
            <WfText class="home__featured-copy">从祭祀礼器到日常用具，梳理商周青铜文明的工艺演进与社会礼制。</WfText>
            <WfRow class="museum-meta-row home__featured-meta" :gap="12">
              <WfText class="home__featured-meta-item">128 件展品</WfText>
              <WfText class="home__featured-meta-item">一层东厅</WfText>
              <WfText class="home__featured-meta-item">约 90 分钟</WfText>
            </WfRow>
          </WfColumn>
        </WfCard>

        <WfRow id="home-quick-actions" class="home__quick-actions" :gap="10">
          <WfButton id="home-map-action" class="home__map-action" to="floor-map">楼层导览</WfButton>
          <WfButton id="home-exhibitions-action" class="home__exhibitions-action" variant="primary" to="exhibitions">全部展厅</WfButton>
        </WfRow>

        <WfHeading id="home-exhibitions-title" class="museum-section-heading home__exhibitions-title" :level="2">在展专题</WfHeading>
        <WfGrid id="home-exhibitions" class="home__exhibitions" :columns="1" :gap="14">
          <WfCard
            v-for="(item, index) in exhibitions"
            :key="item.id"
            class="museum-card home__exhibition-card"
            :data-wf-key="item.id"
            to="exhibition-detail"
          >
            <WfImagePlaceholder class="home__exhibition-image" :height="index % 2 === 0 ? 112 : 128" :border-radius="0" />
            <WfColumn class="museum-card__body home__exhibition-body" :gap="6">
              <WfHeading class="home__exhibition-title" :level="3">{{ item.title }}</WfHeading>
              <WfText class="home__exhibition-meta">{{ item.period }}</WfText>
              <WfText class="home__exhibition-note">{{ item.hall }} · {{ item.note }}</WfText>
            </WfColumn>
          </WfCard>
        </WfGrid>

        <WfHeading id="home-highlights-title" class="museum-section-heading home__highlights-title" :level="2">镇馆精选</WfHeading>
        <WfColumn id="home-highlights" class="home__highlights" :gap="0">
          <WfCell
            v-for="item in highlights"
            :key="item.id"
            class="home__highlight"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.era + ' · ' + item.hall"
            to="artifact-detail"
          />
        </WfColumn>
      </WfColumn>
    </WfMobileLayout>
  `,
}))
