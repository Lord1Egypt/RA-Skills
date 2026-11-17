const EMPTY_BANK={name:'',account:'',bank:''};
export default {
inject:['service', 'tags'],
data() {return {
    list:[],
    ctrl:{dlg:false,dta:{},cur:1,max:0,opts:[],no:-1,search:''}
}},
created(){
    var bt=this.tags.bankType;
    this.ctrl.opts=[{value:'PER',label:bt.PER},{value:'ENT',label:bt.ENT}];
    this.query(1);
},
methods:{
query(pg){
    var offset=(parseInt(pg)-1)*this.service.N_PAGE;
    var opts={method:"GET", url:"/bankacc/list?offset="+offset+"&num="+this.service.N_PAGE};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.list=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        this.list=resp.data.list.map(b=>{
            b.type_s=this.tags.bankType[b.type];
            return b;
        });
        this.ctrl.max=Math.ceil(resp.data.total/this.service.N_PAGE);
    })
},
search(){
    var opts={method:"GET", url:"/bankacc/search?s="+this.ctrl.search+"&limit="+this.service.N_PAGE};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.list=[];
            this.ctrl.max=0;
            this.ctrl.cur=1;
            return;
        }
        this.list=resp.data.list.map(b=>{
            b.type_s=this.tags.bankType[b.type];
            return b;
        });
        this.ctrl.max=1;
        this.ctrl.cur=1;
    })    
},
show_bank(i) {
    if(i>-1) {
        this.ctrl.tag=this.tags.modify;
        copyObjTo(this.list[i], this.ctrl.dta);
    } else {
        this.ctrl.tag=this.tags.add;
        copyObjTo(EMPTY_BANK, this.ctrl.dta);
    }
    this.ctrl.no=i;
    this.ctrl.dlg=true;
},
bank_do() {
    var opts;
    if(this.ctrl.no>-1){
        opts={method:"PUT",url:"/bankacc/update",data:this.ctrl.dta};
    } else {
        opts={method:"POST",url:"/bankacc/add",data:this.ctrl.dta};
    }
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query(this.ctrl.cur);
        this.ctrl.dlg=false;
        this.ctrl.no=-1;
    })
},
bank_remove() {
    if(this.ctrl.no<0)return;
    var d=this.ctrl.dta;
    var opts={method:"DELETE",url:"/bankacc/remove?id="+d.id+"&type="+d.type};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query(this.ctrl.cur);
        this.ctrl.dlg=false;
        this.ctrl.no=-1;
    })
},
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.bank.title}}</q-toolbar-title>
   </q-toolbar>
  </q-header>
  <q-footer class="bg-white q-pa-md">
    <q-input outlined v-model="ctrl.search" :label="tags.search" dense @keyup.enter="search">
     <template v-slot:append>
      <q-icon v-if="ctrl.search!==''" name="close" @click="query(1)" class="cursor-pointer"></q-icon>
      <q-icon name="search" @click="search"></q-icon>
     </template>
     <template v-slot:after>
      <q-btn round color="primary" icon="add_circle" @click="show_bank(-1)"></q-btn>
     </template>
    </q-input>
  </q-footer>
  <q-page-container>
    <q-page class="q-pa-md">
<div class="q-pa-sm flex flex-center" v-show="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-list separator>
 <q-item>
  <q-item-section><q-item-label caption>{{tags.bank.bank}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.bank.name}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.bank.account}}</q-item-label></q-item-section>
  <q-item-section side><q-item-label caption>{{tags.bank.type}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="(b,i) in list" clickable @click="show_bank(i)">
  <q-item-section>{{b.bank}}</q-item-section>
  <q-item-section>{{b.name}}</q-item-section>
  <q-item-section>{{b.account}}</q-item-section>
  <q-item-section side>{{b.type_s}}</q-item-section>
 </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="ctrl.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{ctrl.tag}}</div>
  </q-card-section>
  <q-card-section class="q-pt-sm">
   <q-option-group v-model="ctrl.dta.type" :options="ctrl.opts"
    color="primary" inline type="radio" :disable="ctrl.no>-1"></q-option-group>
   <q-input :label="tags.bank.bank" v-model="ctrl.dta.bank" dense></q-input>
   <q-input :label="tags.bank.name" v-model="ctrl.dta.name" dense></q-input>
   <q-input :label="tags.bank.account" v-model="ctrl.dta.account" dense></q-input>
  </q-card-section>
  <q-card-actions class="row">
   <div class="col text-left" v-if="ctrl.no>-1">
    <q-btn :label="tags.remove" color="red" @click="bank_remove" flat></q-btn>
   </div>
   <div class="col text-right">
    <q-btn :label="tags.ok" color="primary" @click="bank_do"></q-btn>
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
   </div>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
`
}