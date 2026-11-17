//一边输入名称，一边过滤供应商的组件
export default {
data() {return {opts:[],oldLen:0}},
props: {
    modelValue:{type:Object,required:true},
    label:{type:String,required:true},
    factory:{type:Number,required:true},
    num:{type:Number,required:false,default:5}
},
emits: ['update:modelValue'],
methods:{
get_opts(val,update) {
  var ol=this.oldLen;
  this.oldLen=val.length;
  if(val==='') {
    update(() => {
      this.opts=[]
    })
    return;
  }
  update(() => {
    if(val.length>1) {
      if(ol>0 && this.opts.length==0 && val.length>ol) {
        return;//已有的输入找不到，更多的输入更找不到
      }
    }
    var opts={method:"GET",url:"/api/resource/search?limit="
        +this.num+"&no="+val+"&factory="+this.factory};
    request(opts, "iresource").then(resp => {
        if(resp.code!=RetCode.OK) {
            this.opts=[]
            return;
        }
        var opts=[];
        var name;
        for(var l of resp.data.list) {//no,sku,skuName,num,price,inDate
            name=l.no + '(' + l.skuName + ',' + l.num + '/' + l.price + ')';
            opts.push({value:l.no, label:name});
        }
        this.opts=opts;
    })
  })
}
},
computed: {
  value: {
      get() {
        var v=this.modelValue;
        return {value:v.id, label:v.name};
      },
      set(v) {
        this.$emit('update:modelValue', {no:v.value, name:v.label});
      }
  }
},
template: `
<q-select v-model="value" :label="label" :options="opts"
  use-input input-debounce="200" dense hide-dropdown-icon
  :multiple=false @filter="get_opts">
  <template v-slot:no-option>
   <q-item><q-item-section class="text-grey">
     No options
   </q-item-section></q-item>
  </template>
</q-select>
`
}