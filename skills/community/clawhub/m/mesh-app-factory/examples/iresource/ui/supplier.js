const EMPTY_SUPPLIER={name:'',taxid:'',cmt:'',addr:'',business:''};
export default {
inject:['service', 'tags'],
data() {return {
    suppliers:[],
    ctrl:{dlg:false,dta:{},cur:1,max:0}
}},
created(){
    this.query(1);
},
methods:{
query(pg){
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var opts={method:"GET", url:"/supplier/list?offset="+offset+"&num="+this.service.N_PAGE};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.suppliers=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        var dt=new Date();
        for(var s of resp.data.list) {
            dt.setTime(s.createAt*60000);
            s.createAt_s=date2str(dt);
        }
        this.suppliers=resp.data.list;
        this.ctrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
show_add() {
    copyObjTo(EMPTY_SUPPLIER, this.ctrl.dta);
    this.ctrl.dlg=true;
},
create() {
    var opts={method:"POST",url:"/supplier/add",data:this.ctrl.dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query(this.ctrl.cur);
        this.ctrl.dlg=false;
    });
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.supplier.title}}</q-toolbar-title>
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
  <q-item-section><q-item-label caption>{{tags.name}}/{{tags.supplier.addr}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.supplier.creator}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.cmt}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="(s,i) in suppliers" clickable @click="service.goto('/supdetail?id='+s.id)">
  <q-item-section>
   <q-item-label>{{s.name}}</q-item-label>
   <q-item-label caption>{{s.addr}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{s.creator}}</q-item-label>
   <q-item-label caption>{{s.createAt_s}}</q-item-label>
  </q-item-section>
  <q-item-section>
   <q-item-label>{{s.cmt}}</q-item-label>
   <q-item-label caption>{{s.business}}</q-item-label>
  </q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{tags.add}}</div>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <q-input :label="tags.name" v-model="ctrl.dta.name" dense></q-input>
   <q-input :label="tags.supplier.addr" v-model="ctrl.dta.addr" dense></q-input>
   <q-input :label="tags.supplier.taxid" v-model="ctrl.dta.taxid" dense></q-input>
   <q-input :label="tags.supplier.business" v-model="ctrl.dta.business" dense></q-input>
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