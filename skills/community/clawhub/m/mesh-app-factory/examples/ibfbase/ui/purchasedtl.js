import AlertDialog from "/assets/v3/components/alert_dialog.js";
import ConfirmDialog from "/assets/v3/components/confirm_dialog.js";
import DateInput from "/assets/v3/components/date_input.js"
import SkuSelector from "./components/sku_selector.js"
import {sta2icon} from '/assets/v3/components/workflow.js';

export default {
inject:["ibf"],
components:{
    "alert-dialog":AlertDialog,
    "confirm-dialog":ConfirmDialog,
    "date-input":DateInput,
    "sku-select":SkuSelector
},
data() {return {
    id:this.$route.query.id,
    tags:this.ibf.tags,
    editable:false,
    editing:false,
    dtl:{},
    edtDtl:{}, //编辑内容
    skuList:[],
    skuCtrl:{dlg:false, dta:{}}
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
            this.skuList=p.skus;
        } else {
            this.skuList=[];
        }
        delete p.skus;
        //cost,expDate,flSta,flowid,applicant,
        //receiver,descr,pid,prjName,power
        var dt=new Date();
        dt.setTime(p.expDate*60000);
        p.expDate_s=date2str(dt);
        p.staIcon=sta2icon(p.status);
        p.type=this.tags.purchase.types[p.type];
        if(p.cost<=0) p.cost=this.tags.purchase.notCalcu;
        if(p.grn) {//state,inDate,outDate,execAcc,cmt
            var g=p.grn;
            dt.setTime(g.inDate*60000);
            g.inDate=datetime2str(dt);
            dt.setTime(g.outDate*60000);
            g.outDate=datetime2str(dt);
            g.state=this.tags.grn.state[g.state];
        }      
        if(p.gdn) {//state,outDate,cfmDate,tranNo,cmt
            var g=p.gdn;
            dt.setTime(g.cfmDate*60000);
            g.cfmDate=datetime2str(dt);
            dt.setTime(g.outDate*60000);
            g.outDate=datetime2str(dt);
            g.state=this.tags.gdn.state[g.state];
        }      
        this.dtl=p;
        this.editable=p.status==0;
    })
},
show_sku() {
    this.skuCtrl.dta={sku:{id:'',name:''},num:''};
    this.skuCtrl.dlg=true;
},
add_sku() {
    var d=this.skuCtrl.dta;
    if(!d.sku.id||!d.num)return;
    var dta={sku:d.sku.id,skuName:d.sku.name,num:d.num,
        purId:this.id,flowid:this.dtl.flowid};

    var opts={method:"POST", url:"/purchase/addSku", data:dta};
    request(opts, this.ibf.SERVICE_RES).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        dta.price=0;
        this.skuList.push(dta);
        this.skuCtrl.dlg=false;
    });
},
remove_sku(i) {
    var url="/purchase/removeSku?purId="+this.id
        +"&flowid="+this.dtl.flowid+"&sku="+this.skuList[i].sku;
    request({method:"DELETE", url:url}, this.ibf.SERVICE_RES).then(resp => {
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.skuList.splice(i,1);
    });
},
show_edit() {
    this.editing=true;
    copyObjTo(this.dtl, this.edtDtl);
},
update() {
    var dta=copyObj(this.edtDtl,['expDate','receiver','descr']);
    dta.id=this.id;
    dta.flowid=this.dtl.flowid;
    request({method:"PUT", url:"/purchase/update", data:dta}, this.ibf.SERVICE_RES).then(resp=>{
        if(resp.code != RetCode.OK) {
            this.$refs.alertDlg.showErr(resp.code, resp.info);
            return;
        }
        this.editing=false;
        copyObjTo(this.edtDtl, this.dtl, ['expDate','receiver','descr']);
    });
},
remove() {
    this.$refs.cfmDlg.show(this.tags.cfmRmv, ()=>{
        var opts={method:"DELETE",url:"/purchase/remove?id="+this.id+"&flowid="+this.dtl.flowid};
        request(opts, this.ibf.SERVICE_RES).then(resp => {
            if(resp.code!=RetCode.OK) {
                this.$refs.alertDlg.showErr(resp.code, resp.info);
                return;
            }
            this.ibf.back();
        })
    });
},
pur_flow() {
    this.ibf.showFlow(this.dtl.flowid, this.id,
        '/ibf/workflow?service='+this.ibf.SERVICE_RES);
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.purchase.title}}({{dtl.type}})</q-toolbar-title>
     <q-btn flat icon="clear" @click="remove()" v-if="editable" dense></q-btn>
     <q-btn flat icon="edit" @click="show_edit" v-if="editable&&!editing" dense></q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-none">
<q-list dense>
  <q-item>
    <q-item-section>{{tags.purchase.applicant}}</q-item-section>
    <q-item-section side>{{dtl.applicant}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.purchase.cost}}</q-item-section>
    <q-item-section side>{{dtl.cost}}</q-item-section>
  </q-item>
  <q-item clickable @click.stop="pur_flow">
    <q-item-section class="text-blue">{{tags.purchase.status}}</q-item-section>
    <q-item-section side><q-icon :name="dtl.staIcon" color="blue"></q-icon></q-item-section>
  </q-item>
</q-list>
<q-list dense v-if="!editing">
  <q-item>
    <q-item-section>{{tags.purchase.receiver}}</q-item-section>
    <q-item-section side>{{dtl.receiver}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.purchase.expDate}}</q-item-section>
    <q-item-section side>{{dtl.expDate_s}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.cmt}}</q-item-section>
   <q-item-section side>{{dtl.descr}}</q-item-section>
  </q-item>
</q-list>
<div v-else>
  <q-input v-model="edtDtl.receiver" :label="tags.purchase.receiver"></q-input>
  <date-input v-model="edtDtl.expDate_s" :label="tags.purchase.expDate"
  :format="tags.dateFmt"></date-input>
  <q-input v-model="edtDtl.descr" :label="tags.cmt"></q-input>
  <div class="row justify-end q-py-md">
    <div class="col-2">
      <q-btn flat :label="tags.cancel" @click="editing=false" color="primary"></q-btn>
    </div>
    <div class="col-2">
      <q-btn :label="tags.ok" @click="update" color="primary"></q-btn>
    </div>
  </div>
</div>
<q-separator></q-separator>
<q-list separator>
<q-item v-if="dtl.grn">
 <q-item-section>
  <q-item-label>{{tags.grn.title}} {{dtl.grn.tranNo}}</q-item-label>
  <q-item-label caption>{{dtl.grn.execAcc}}/{{dtl.grn.inDate}}</q-item-label>
  <q-item-label caption>{{dtl.grn.cmt}}</q-item-label>
 </q-item-section>
 <q-item-section side>
  <q-item-label>{{dtl.grn.state}}</q-item-label>
  <q-item-label caption>{{dtl.grn.outDate}}</q-item-label>
 </q-item-section>
</q-item>
<q-item v-if="dtl.gdn">
 <q-item-section>
  <q-item-label>{{tags.gdn.title}} {{dtl.gdn.tranNo}}</q-item-label>
  <q-item-label caption>{{dtl.gdn.execAcc}}/{{dtl.gdn.cfmDate}}</q-item-label>
  <q-item-label caption>{{dtl.gdn.cmt}}</q-item-label>
 </q-item-section>
 <q-item-section side>
  <q-item-label>{{dtl.gdn.state}}</q-item-label>
  <q-item-label caption>{{dtl.gdn.outDate}}</q-item-label>
 </q-item-section>
</q-item>
</q-list>

<q-banner inline-actions dense class="q-mb-sm text-dark bg-blue-grey-1">
  {{tags.purchase.skuList}}
  <template v-slot:action v-if="dtl.status==0">
    <q-icon name="add_circle" @click="show_sku" color="primary"></q-icon>
  </template>
</q-banner>
<q-list dense separator>
  <q-item>
   <q-item-section><q-item-label caption>{{tags.purchase.sku}}</q-item-label></q-item-section>
   <q-item-section><q-item-label caption>{{tags.num}}</q-item-label></q-item-section>
   <q-item-section><q-item-label caption>{{tags.price}}</q-item-label></q-item-section>
   <q-item-section side></q-item-section>
  </q-item>
  <q-item v-for="(e,i) in skuList">
   <q-item-section>{{e.skuName}}</q-item-section>
   <q-item-section>{{e.num}}</q-item-section>
   <q-item-section>{{e.price}}</q-item-section>
   <q-item-section side v-if="editable">
    <q-btn icon="clear" @click="remove_sku(i)" flat dense color="red"></q-btn>
   </q-item-section>
  </q-item>
</q-list>
    </q-page>
  </q-page-container>
</q-layout>

<q-dialog v-model="skuCtrl.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
   <div class="text-h6">{{tags.purchase.skuList}}</div>
   <q-separator></q-separator>
  </q-card-section>
  <q-card-section class="q-pt-none">
    <sku-select v-model="skuCtrl.dta.sku" :label="tags.purchase.sku"></sku-select>
    <q-input v-model.number="skuCtrl.dta.num" :label="tags.num"></q-input>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="add_sku"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="alertDlg"></alert-dialog>
<confirm-dialog :title="tags.attention" :ok="tags.ok"
 :close="tags.cancel" ref="cfmDlg"></confirm-dialog>
`
}