/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('search', ({ ref, computed }) => ({
  setup() {
    const keyword = ref('')
    const category = ref('all')
    const categories = [
      { id: 'all', label: '全部' },
      { id: 'bronze', label: '青铜' },
      { id: 'porcelain', label: '瓷器' },
      { id: 'calligraphy', label: '书画' },
      { id: 'jade', label: '玉器' },
    ]
    const catalog = [
      { id: 'art-ding', title: '兽面纹青铜鼎', category: 'bronze', era: '商代晚期', hall: '一层东厅' },
      { id: 'art-zun', title: '鸮形青铜尊', category: 'bronze', era: '商代', hall: '一层东厅' },
      { id: 'art-vase', title: '青花缠枝莲瓶', category: 'porcelain', era: '明永乐', hall: '二层南厅' },
      { id: 'art-bowl', title: '粉彩花卉碗', category: 'porcelain', era: '清乾隆', hall: '二层南厅' },
      { id: 'art-scroll', title: '行书快雪时晴摹本', category: 'calligraphy', era: '清代', hall: '三层西厅' },
      { id: 'art-landscape', title: '山水长卷', category: 'calligraphy', era: '明代', hall: '三层西厅' },
      { id: 'art-jade', title: '和田白玉璧', category: 'jade', era: '汉代', hall: '二层北厅' },
      { id: 'art-pendant', title: '龙凤纹玉佩', category: 'jade', era: '战国', hall: '二层北厅' },
      { id: 'art-mirror', title: '四神纹铜镜', category: 'bronze', era: '汉代', hall: '一层东厅' },
      { id: 'art-plate', title: '釉里红大盘', category: 'porcelain', era: '元末明初', hall: '二层南厅' },
    ]
    const results = computed(() => {
      const query = keyword.value.trim()
      return catalog.filter((item) => {
        const matchCategory = category.value === 'all' || item.category === category.value
        const matchKeyword = !query || item.title.includes(query) || item.era.includes(query) || item.hall.includes(query)
        return matchCategory && matchKeyword
      })
    })
    return { keyword, category, categories, results }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="search-page" class="museum-page search__page" :gap="16">
        <WfPageHeader
          id="search-header"
          title-id="search-title"
          class="search__header"
          title="搜索展品"
          subtitle="按名称、时代或展厅筛选"
        />

        <WfTextInput
          id="search-input"
          v-model="keyword"
          class="search__input"
          placeholder="输入展品名称或时代"
        />

        <WfTabs id="search-categories" v-model:active-id="category" class="search__categories" :items="categories" />

        <WfText id="search-result-count" class="search__result-count">共 {{ results.length }} 条结果</WfText>

        <WfColumn id="search-results" class="search__results" :gap="0">
          <WfCell
            v-for="item in results"
            :key="item.id"
            class="search__result"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.era + ' · ' + item.hall"
            to="artifact-detail"
          />
        </WfColumn>

        <WfEmptyState
          v-if="results.length === 0"
          id="search-empty"
          class="search__empty"
          title="未找到匹配展品"
          description="尝试更换关键词或切换分类"
        />
      </WfColumn>
    </WfMobileLayout>
  `,
}))
