(function defineShanghaiMap({ defineComponent }) {
  defineComponent('WfShanghaiMap', () => ({
    template: `<WfWireMap class="shanghai-map"><slot /></WfWireMap>`,
  }))
})(window.WireframeVue)
