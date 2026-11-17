const EMPTY_FAC={name:'',addr:'',cmt:'',createAt:''};
export default {
inject:['service', 'tags'],
data() {return {
    factories:[], //工厂
    ctrl:{dlg:false,dta:{}}
}},
created(){
    this.query();
},
methods:{
query(){
    var opts={method:"GET", url:"/factory/list"}
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.factories=[];
            return;
        }
        var dt=new Date();
        for(var f of resp.data.list) {
            dt.setTime(f.createAt*60000);
            f.createAt_s=date2str(dt);
        }
        this.factories=resp.data.list;
    })  
},
show_add() {
    copyObjTo(EMPTY_FAC, this.ctrl.dta);
    this.ctrl.dlg=true;
},
create() {
    var opts={method:"POST",url:"/factory/add",data:this.ctrl.dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.query();
        this.ctrl.dlg=false;
    });
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat round icon="arrow_back" dense @click="service.back()"></q-btn>
     <q-toolbar-title>{{tags.factory.title}}</q-toolbar-title>
     <q-btn flat icon="add_circle" @click="show_add"></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-md">
<q-list separator>
 <q-item>
  <q-item-section><q-item-label caption>{{tags.name}}/{{tags.factory.addr}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.createAt}}</q-item-label></q-item-section>
  <q-item-section><q-item-label caption>{{tags.cmt}}</q-item-label></q-item-section>
 </q-item>
 <q-item v-for="f in factories" clickable @click="service.goto('/facdetail?id='+f.id)">
  <q-item-section>
   <q-item-label>{{f.name}}</q-item-label>
   <q-item-label caption>{{f.addr}}</q-item-label>
  </q-item-section>
  <q-item-section>{{f.createAt_s}}</q-item-section>
  <q-item-section>{{f.cmt}}</q-item-section>
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
   <q-input :label="tags.factory.addr" v-model="ctrl.dta.addr" dense></q-input>
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