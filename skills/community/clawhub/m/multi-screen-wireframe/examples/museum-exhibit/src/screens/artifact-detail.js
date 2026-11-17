/**
 * @wireframe-skill multi-screen-wireframe@2.0.0
 * 创建基于 v2.0.0
 * 修改基于 v2.0.0
 */
WireframeVue.defineScreen('artifact-detail', ({ ref, onUnmounted }) => ({
  setup() {
    const audioOn = ref(false)
    const favorited = ref(false)
    const toastOpen = ref(false)
    let toastTimer = null

    function toggleFavorite() {
      favorited.value = !favorited.value
      if (favorited.value) {
        toastOpen.value = true
        if (toastTimer) clearTimeout(toastTimer)
        toastTimer = setTimeout(() => {
          toastOpen.value = false
          toastTimer = null
        }, 2000)
      }
    }

    onUnmounted(() => {
      if (toastTimer) clearTimeout(toastTimer)
    })

    return {
      audioOn,
      favorited,
      toastOpen,
      toggleFavorite,
      breadcrumbs: [{ label: '青铜时代', to: 'exhibition-detail' }, { label: '兽面纹青铜鼎' }],
      specs: [
        { label: '时代', value: '商代晚期' },
        { label: '材质', value: '青铜' },
        { label: '尺寸', value: '高 42.5 cm' },
        { label: '出土地', value: '河南安阳' },
      ],
      related: [
        { id: 'art-zun', title: '鸮形青铜尊', era: '商代' },
        { id: 'art-vessel', title: '夔龙纹青铜簋', era: '西周' },
        { id: 'art-mirror', title: '四神纹铜镜', era: '汉代' },
      ],
    }
  },
  template: /*html*/ `
    <WfMobileLayout>
      <WfColumn id="artifact-detail-page" class="museum-page artifact-detail__page" :gap="18">
        <WfBreadcrumbs id="artifact-detail-breadcrumbs" class="artifact-detail__breadcrumbs" :items="breadcrumbs" />

        <WfImagePlaceholder id="artifact-detail-hero" class="artifact-detail__hero" :height="240" :border-radius="0" />

        <WfColumn id="artifact-detail-summary" class="artifact-detail__summary" :gap="10">
          <WfHeading id="artifact-detail-title" class="artifact-detail__title" :level="1">兽面纹青铜鼎</WfHeading>
          <WfText class="artifact-detail__subtitle">一层东厅 · 03 号柜 · 编号 BZ-0271</WfText>
          <WfRow class="museum-chip-row artifact-detail__badges" :gap="8">
            <WfBadge class="artifact-detail__badge">国宝级</WfBadge>
            <WfBadge class="artifact-detail__badge">禁止出境</WfBadge>
          </WfRow>
        </WfColumn>

        <WfCard id="artifact-detail-audio" class="artifact-detail__audio">
          <WfRow class="artifact-detail__audio-row" :gap="12" align-items="center" justify-content="space-between">
            <WfColumn :gap="4">
              <WfHeading class="artifact-detail__audio-title" :level="3">语音导览</WfHeading>
              <WfText class="artifact-detail__audio-copy">时长 3 分 18 秒 · 中文讲解</WfText>
            </WfColumn>
            <WfToggle id="artifact-detail-audio-toggle" v-model:checked="audioOn" label="播放语音导览" />
          </WfRow>
        </WfCard>

        <WfGrid id="artifact-detail-specs" class="artifact-detail__specs" :columns="2" :gap="8">
          <WfCard
            v-for="item in specs"
            :key="item.label"
            class="artifact-detail__spec"
            :data-wf-key="item.label"
          >
            <span class="artifact-detail__spec-label">{{ item.label }}</span>
            <span class="artifact-detail__spec-value">{{ item.value }}</span>
          </WfCard>
        </WfGrid>

        <WfCard id="artifact-detail-description" class="artifact-detail__description">
          <WfColumn :gap="10">
            <WfHeading class="artifact-detail__description-title" :level="3">展品说明</WfHeading>
            <WfText class="artifact-detail__description-copy">此鼎腹部饰兽面纹，立耳、深腹、三足，为商代王室祭祀用器。纹样以浮雕方式呈现，线条规整，是研究商代青铜铸造与礼制的重要实物。</WfText>
            <WfText class="artifact-detail__description-copy">鼎内壁可见三组铭文，记录了器物的归属与使用场合，对断代具有关键价值。</WfText>
          </WfColumn>
        </WfCard>

        <WfHeading id="artifact-detail-related-title" class="museum-section-heading artifact-detail__related-title" :level="2">相关展品</WfHeading>
        <WfColumn id="artifact-detail-related" class="artifact-detail__related" :gap="0">
          <WfCell
            v-for="item in related"
            :key="item.id"
            class="artifact-detail__related-item"
            :data-wf-key="item.id"
            :title="item.title"
            :subtitle="item.era"
            to="artifact-detail"
          />
        </WfColumn>

        <WfRow id="artifact-detail-actions" class="artifact-detail__actions" :gap="10">
          <WfButton id="artifact-detail-map-action" class="artifact-detail__map-action" to="floor-map">定位展厅</WfButton>
          <WfButton
            id="artifact-detail-favorite-action"
            class="artifact-detail__favorite-action"
            variant="primary"
            @click="toggleFavorite"
          >{{ favorited ? '已收藏' : '加入收藏' }}</WfButton>
        </WfRow>

        <WfToast :open="toastOpen" label="已加入收藏" />
      </WfColumn>
    </WfMobileLayout>
  `,
}))
