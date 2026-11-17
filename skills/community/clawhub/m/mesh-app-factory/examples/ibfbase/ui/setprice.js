import AlertDialog from "/assets/v3/components/alert_dialog.js";

export default {
inject:["ibf"],
components:{
    "alert-dialog":AlertDialog
},
data() {return {
    id:this.$route.query.did,
    tags:this.ibf.tags,
    dtl:{},
    skus:[],
    ctrl:{sku:0,suppliers:[]}//当前选中的采购项的所有供应商及报价
}},
created(){
    this.query();
},
methods:{
query() {
    var url="/purchase/detail?id="+this.id;
    request({method:"GET", url:url}, this.ibf.SERVICE_RES).then(resp => {
        if(resp.code!=RetCode.OK) {
            return;
        }
        var p=resp.data;
        if(p.skus) { //sku,num,price,skuName
            this.skus=p.skus;
        } else {
            this.skus=[];
        }
        delete p.skus;
        //cost,expDate,flSta,flowid,applicant,
        //receiver,descr,pid,prjName,power
        var dt=new Date();
        dt.setTime(p.expDate*60000);
        p.expDate_s=date2str(dt);
        if(p.cost<=0) p.cost=this.tags.purchase.notCalcu;
        this.dtl=p;
    })
},
get_suppliers(sku) {
    var opts={method:"GET", url:"/sku/listSupplier?id="+sku};
    request(opts, this.ibf.SERVICE_RES).then(resp => {
        if(resp.code != RetCode.OK) {
            this.ctrl.suppliers=[];
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.ctrl.sku=sku;
        this.ctrl.suppliers=resp.data.list;
    }); 
},
set_price(val, oldVal) {
    if(val==oldVal)return;
    var dta={sku:this.ctrl.sku,price:val,purId:this.id};

    var opts={method:"PUT", url:"/purchase/setPrice", data:dta};
    request(opts, this.ibf.SERVICE_RES).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.dtl.cost=resp.data.cost;
    });
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.purchase.title}}</q-toolbar-title>
     <q-btn flat icon="clear" @click="remove()" v-if="editable" dense></q-btn>
     <q-btn flat icon="edit" @click="show_edit" v-if="editable&&!editing" dense></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-sm">
<q-list dense>
  <q-item>
    <q-item-section>{{tags.purchase.applicant}}</q-item-section>
    <q-item-section side>{{dtl.applicant}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.purchase.cost}}</q-item-section>
    <q-item-section side>{{dtl.cost}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.purchase.expDate}}</q-item-section>
    <q-item-section side>{{dtl.expDate_s}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.purchase.receiver}}</q-item-section>
    <q-item-section side>{{dtl.receiver}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.cmt}}</q-item-section>
   <q-item-section side>{{dtl.descr}}</q-item-section>
  </q-item>
</q-list>
<q-banner inline-actions dense class="bg-indigo-3 text-white">
  {{tags.purchase.skuList}}
</q-banner>
<q-list dense separator>
  <q-item v-for="(e,i) in skus">
   <q-item-section>{{e.skuName}}</q-item-section>
   <q-item-section>{{e.num}}</q-item-section>
   <q-item-section>{{e.price}}</q-item-section>
   <q-item-section avatar>
    <q-icon name="edit" color="primary"></q-icon>
     <q-popup-edit v-model="e.price" v-slot="scope"
      @save="set_price" @before-show="get_suppliers(e.sku)">
      <q-input v-model.number="scope.value" dense autofocus @keyup.enter="scope.set">
       <template v-slot:append>
        <q-icon name="save" color="primary" @click="scope.set"></q-icon>
       </template>
      </q-input>
      <q-list dense>
       <q-item v-for="s in ctrl.suppliers" clickable
        @click="scope.value=s.price;scope.set();">
        <q-item-section>{{s.name}}</q-item-section>
        <q-item-section side>{{s.price}}</q-item-section>
       </q-item>
      </q-list>
     </q-popup-edit>
   </q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>
<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>
`
}