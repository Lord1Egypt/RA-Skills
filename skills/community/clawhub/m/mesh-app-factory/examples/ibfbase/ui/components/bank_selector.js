//一边输入名称，一边过滤银行帐号的组件，银行帐号必须已输入ifinance
export default {
data() {return {opts:{value:[]},v:null,oldLen:0}},
props: {
    modelValue:{type:String,required:true},
    label:{type:String,required:false,default:''}
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
    var opts={method:"GET",url:"/api/bankacc/search?limit=10&s="+val};
    request(opts, "ifinance").then(resp => {
        if(resp.code!=RetCode.OK) {
            this.opts=[]
            return;
        }
        var opts=[];
        for(var s of resp.data.list) {
            opts.push(s.bank+':'+s.account+','+s.name);
        }
        this.opts=opts;
    })
  })
},
input_val(val) {
    this.v=val;
    this.$emit('update:modelValue', this.v);
},
changed() {
    this.$emit('update:modelValue', this.v);
}
},
template: `
<q-select v-model="v" :label="label" :options="opts"
  use-input hide-selected fill-input input-debounce="200" dense
  @update:model-value="changed" :multiple=false
  @input-value="input_val" @filter="get_opts">
  <template v-slot:no-option>
   <q-item><q-item-section class="text-grey">
     No options
   </q-item-section></q-item>
  </template>
</q-select>
`
}