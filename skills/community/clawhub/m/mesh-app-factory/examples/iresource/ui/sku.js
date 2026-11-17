const EMPTY_SKU={name:'',speci:'',cmt:'',createAt:'',type:'',noHead:'',yearDepr:'',monthDepr:''};
export default {
inject:['service', 'tags'],
data() {return {
    skus:[],
    ctrl:{dlg:false,dta:{},cur:1,max:0,skuTypes:[]}
}},
created(){
    this.query(1);
    for(var i in this.tags.skuType) {
        this.ctrl.skuTypes.push({label:this.tags.skuType[i],value:i});
    }
},
methods:{
query(pg){
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var opts={method:"GET", url:"/sku/list?offset="+offset+"&num="+this.service.N_PAGE};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.skus=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        var dt=new Date();
        for(var s of resp.data.list) {
            dt.setTime(s.createAt*60000);
            s.createAt_s=date2str(dt);
            s.type_s=this.tags.skuType[s.type];
        }
        this.skus=resp.data.list;
        this.ctrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
show_add() {
    this.ctrl.tag=this.tags.add;
    copyObjTo(EMPTY_SKU, this.ctrl.dta);
    this.ctrl.dlg=true;
},
create() {
    var opts={method:"POST",url:"/sku/add",data:this.ctrl.dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query(this.ctrl.cur);
        this.ctrl.dlg=false;
    });
},
monDeprChanged() {
    if(this.ctrl.dta.yearDepr!='') {
        return; //已设置了，不自动变化
    }
    var yd=this.ctrl.dta.monthDepr*12;
    this.ctrl.dta.yearDepr=yd.toFixed(2);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.sku.title}}</q-toolbar-title>
     <q-btn flat icon="add_circle" @click="show_add"></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-show="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-list separator>
 <q-item>
  <q-item-section><q-item-label caption>{{tags.name}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.sku.type}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.createAt}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.cmt}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="(s,i) in skus" clickable @click="service.goto('/skudetail?id='+s.id)">
  <q-item-section>
   <q-item-label>{{s.name}}</q-item-label>
   <q-item-label caption>{{s.speci}}</q-item-label>
  </q-item-section>
  <q-item-section>{{s.type_s}}</q-item-section>
  <q-item-section>{{s.createAt_s}}</q-item-section>
  <q-item-section>
   <q-item-label>{{s.cmt}}</q-item-label>
   <q-item-label caption>
    {{s.noHead}}/{{s.monthDepr}}/{{s.yearDepr}}
   </q-item-label>
  </q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.dlg" persistent>
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{tags.add}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-input :label="tags.name" v-model="ctrl.dta.name" dense></q-input>
   <q-select :label="tags.sku.type" v-model="ctrl.dta.type" :options="ctrl.skuTypes" emit-value map-options></q-select>
   <q-input :label="tags.sku.noHead" v-model="ctrl.dta.noHead" dense></q-input>
   <q-input :label="tags.sku.monthDepr" v-model.number="ctrl.dta.monthDepr" dense
   @update:model-value="monDeprChanged" type="number"></q-input>
   <q-input :label="tags.sku.yearDepr" v-model.number="ctrl.dta.yearDepr" dense type="number"></q-input>
   <q-input :label="tags.sku.speci" v-model="ctrl.dta.speci" dense></q-input>
   <q-input :label="tags.cmt" v-model="ctrl.dta.cmt" dense></q-input>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn :label="tags.ok" color="primary" @click="create"></q-btn>
   <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}