//一边输入名称，一边过滤供应商的组件
export default {
data(){return{opts:[],oldLen:0}},
props:{
  modelValue:{type:Object,required:true},
  serviceName:{type:String,required:true},
  label:{type:String,required:true}
},
emits:['update:modelValue'],
methods:{
  get_opts(val,update){
    var ol=this.oldLen;
    this.oldLen=val.length;
    if(val===''){
      update(()=>{
        this.opts=[];
      });
      return;
    }
    update(()=>{
      if(val.length>1){
        if(ol>0&&this.opts.length==0&&val.length>ol){
          return;
        }
      }
      var opts={method:"GET",url:"/api/supplier/search?keyword="+encodeURIComponent(val)};
      request(opts,this.serviceName).then(resp=>{
        if(resp.code!=RetCode.OK){
          this.opts=[];
          return;
        }
        var opts=[];
        for(var s of resp.data.list){
          opts.push({value:s.id,label:s.name});
        }
        this.opts=opts;
      });
    });
  }
},
computed:{
  value:{
    get(){
      var v=this.modelValue;
      return{value:v.id||null,label:v.name||''};
    },
    set(v){
      this.$emit('update:modelValue',{id:v.value,name:v.label});
    }
  }
},
template:`
<q-select v-model="value" :label="label" :options="opts"
  use-input input-debounce="200" dense hide-dropdown-icon
  :multiple=false @filter="get_opts">
  <template v-slot:no-option>
    <q-item><q-item-section class="text-grey">No options</q-item-section></q-item>
  </template>
</q-select>
`
}
