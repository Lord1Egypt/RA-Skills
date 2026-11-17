import BankSelector from "/ibfbase/components/bank_selector.js"
import {sta2icon} from '/assets/v3/components/workflow.js';
import {sysDateToStr} from '/assets/v3/components/datetime_input.js';

const EMPTY_GRN={purId:'',tranNo:'',outDate:'',cmt:''};
const EMPTY_GDN={purId:'',tranNo:''};

export default {
components:{
    "bank-select":BankSelector
},
inject:["tags", "service", "ibf"],
data() {return {
    id:this.$route.query.id,
    editable:false,
    dtl:{},
    skuList:[],
    factory:{opts:[],cur:-1,name:''},//工厂选项
    skuCtrl:{dlg:false,dta:{}},
    grnCtrl:{dlg:false,dta:{}},
    gdnCtrl:{dlg:false,dta:{}},
    payCtrl:{dlg:false,dta:{}}
}},
created(){
    this.query();
    this.service.myFactories().then(ll=>{
        if(ll.length==0) return;
        this.factory.opts=ll;
        this.factory.cur=ll[0].id;
        this.factory.name=ll[0].name;
    });
},
methods:{
query() {
    var url="/purchase/purDetail?id="+this.id;
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
        p.type_s=this.tags.purType[p.type];
        if(p.cost<=0) p.cost=this.tags.purchase.notCalcu;
        if(p.grn) {//id,state,inDate,outDate,execAcc,cmt
            p.grn=p.grn.map(g=>{
                dt.setTime(g.inDate*60000);
                g.inDate=datetime2str(dt);
                dt.setTime(g.outDate*60000);
                g.outDate=datetime2str(dt);
                g.state=this.tags.grn.state[g.state];
                return g
            });
        }
        if(p.gdn) {//id,state,outDate,cfmDate,tranNo,cmt
            p.gdn=p.gdn.map(g=>{;
                dt.setTime(g.cfmDate*60000);
                g.cfmDate=datetime2str(dt);
                dt.setTime(g.outDate*60000);
                g.outDate=datetime2str(dt);
                g.state=this.tags.gdn.state[g.state];
                return g;
            });
        }
        if(p.type=='BUY'){
            p.payState_s=this.tags.payState[p.payState];
        } else {
            p.payState_s='';
            p.payState='OVER'; //简化界面中的判断
        }
        this.dtl=p;
        this.editable=p.state=='PROC';
    })
},
show_grn() {
    copyObjTo(EMPTY_GRN, this.grnCtrl.dta);
    this.grnCtrl.dlg=true;
},
grn_do() {
    var dta=copyObj(this.grnCtrl.dta);
    dta.purId=this.id;
    var outDate=Date.parse(dta.outDate);//ms
    dta.factory=this.factory.cur;
    dta.outDate=parseInt(outDate/60000);
    request({method:"POST",url:"/grn/start",data:dta}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.grnCtrl.dlg=false;
        this.grn_detail(resp.data.id);
    });
},
show_gdn() {
    copyObjTo(EMPTY_GDN, this.gdnCtrl.dta);
    this.gdnCtrl.dlg=true;
},
gdn_do() {
    var dta=copyObj(this.gdnCtrl.dta);
    dta.purId=this.id;
    dta.factory=this.factory.cur;
    request({method:"POST",url:"/gdn/start",data:dta}, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.gdnCtrl.dlg=false;
        this.gdn_detail(resp.data.id);
    });
},
flow() {
    this.ibf.showFlow(this.dtl.flowid, this.id, '/ibf/workflow?service='+this.ibf.SERVICE_RES)
},
apply_pay(){
    if(this.dtl.payState!='INIT')return;
    this.payCtrl.dlg=true;
},
pay_do() {
    var dta=copyObj(this.payCtrl.dta,["bank","cmt"]);
    dta.id=this.id;
    dta.expectAt=parseInt(Date.parse(this.payCtrl.dta.expectAt)/60000);
    var opts={method:"POST",url:"/purchase/pay", data:dta};
    request(opts, this.service.name).then(resp => {
        if(resp.code!=RetCode.OK) {
            this.$refs.errMsg.showErr(resp.code, resp.info);
            return;
        }
        this.dtl.payState='PROC';
        this.dtl.payState_s=this.tags.payState.PROC;
        this.payCtrl.dlg=false;
    })
},
gen_gdnTranNo() {
    var no='';
    if(this.gdnCtrl.dta.tranNo=='') {
        var dt=new Date();
        //确保生成的随机数是8位，如果不足8位，前面补 0
        let r = Math.floor(Math.random()*Math.pow(10, 8));
        no=sysDateToStr(dt,"YYYYMMDDHHmm")+String(r).padStart(8, '0');
    }
    this.gdnCtrl.dta.tranNo=no;
},
gdn_detail(id) {
    this.service.goto('/gdndetail?id='+id+'&factory='+this.factory.cur)
},
grn_detail(id) {
    this.service.goto('/grndetail?id='+id+'&factory='+this.factory.cur)
}
},
template:`
<q-layout view="hHh lpr fFf">
  <q-header>
   <q-toolbar>
     <q-btn flat icon="arrow_back" dense @click="ibf.back()"></q-btn>
     <q-toolbar-title>{{tags.purchase.title}}({{dtl.type_s}})</q-toolbar-title>
     <q-btn flat dense icon-right="factory" :label="factory.name">
       <q-menu>
        <q-list style="min-width:100px">
         <q-item clickable v-close-popup v-for="(f,i) in factory.opts" @click="factory_changed(i)">
           <q-item-section>{{f.name}}</q-item-section>
         </q-item>
        </q-list>
       </q-menu>
     </q-btn>
   </q-toolbar>
  </q-header>
  <q-page-container>
    <q-page class="q-pa-none">
<q-list dense>
  <q-item>
    <q-item-section>{{tags.applicant}}</q-item-section>
    <q-item-section side>{{dtl.applicant}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.purchase.cost}}</q-item-section>
    <q-item-section side @click="apply_pay">
     <div>{{dtl.cost}}
      <q-badge color="primary" v-if="dtl.type=='BUY'">
       {{dtl.payState_s}}
      </q-badge>
     </div>
    </q-item-section>
  </q-item>
  <q-item clickable @click.stop="flow">
    <q-item-section class="text-blue">{{tags.purchase.status}}</q-item-section>
    <q-item-section side><q-icon :name="dtl.staIcon" color="blue"></q-icon></q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.receiver}}</q-item-section>
    <q-item-section side>{{dtl.receiver}}</q-item-section>
  </q-item>
  <q-item>
    <q-item-section>{{tags.expDate}}</q-item-section>
    <q-item-section side>{{dtl.expDate_s}}</q-item-section>
  </q-item>
  <q-item>
   <q-item-section>{{tags.cmt}}</q-item-section>
   <q-item-section side>{{dtl.descr}}</q-item-section>
  </q-item>
</q-list>

<q-banner inline-actions dense class="q-mb-sm text-dark bg-blue-grey-1">
  {{tags.purchase.skuList}}
</q-banner>
<q-list dense separator>
  <q-item>
   <q-item-section><q-item-label caption>{{tags.sku.title}}</q-item-label></q-item-section>
   <q-item-section><q-item-label caption>{{tags.num}}</q-item-label></q-item-section>
   <q-item-section><q-item-label caption>{{tags.sku.price}}</q-item-label></q-item-section>
  </q-item>
  <q-item v-for="(e,i) in skuList">
    <q-item-section>{{e.skuName}}</q-item-section>
    <q-item-section>{{e.num}}</q-item-section>
    <q-item-section>{{e.price}}</q-item-section>
  </q-item>
</q-list>

<div v-if="dtl.type!='BUY'" class="q-pb-sm">
<q-banner inline-actions dense class="q-mb-sm text-dark bg-blue-grey-1">
  {{tags.gdn.title}}
  <template v-slot:action v-if="editable">
   <q-icon color="primary" name="output" @click="show_gdn"></q-icon>
  </template>
</q-banner>
<q-list separator v-if="dtl.gdn">
 <q-item clickable v-for="gdn in dtl.gdn" @click="gdn_detail(gdn.id)">
 <q-item-section>
  <q-item-label>{{gdn.tranNo}}</q-item-label>
  <q-item-label caption>{{gdn.state}}</q-item-label>
 </q-item-section>
 <q-item-section>
  <q-item-label>{{gdn.execAcc}}/{{gdn.cfmDate}}</q-item-label>
  <q-item-label caption>{{gdn.cmt}}</q-item-label>
 </q-item-section>
 <q-item-section side>{{gdn.outDate}}</q-item-section>
 </q-item>
</q-list>
</div>

<div v-if="dtl.type!='SELL'" class="q-pb-sm">
<q-banner inline-actions dense class="q-mb-sm text-dark bg-blue-grey-1">
  {{tags.grn.title}}
  <template v-slot:action v-if="editable">
   <q-icon color="primary" name="exit_to_app" @click="show_grn"></q-icon>
  </template>
</q-banner>
<q-list separator v-if="dtl.grn">
<q-item v-for="grn in dtl.grn" @click="grn_detail(grn.id)" clickable>
 <q-item-section>
  <q-item-label>{{grn.tranNo}}</q-item-label>
  <q-item-label caption>{{grn.state}}</q-item-label>
 </q-item-section>
 <q-item-section>
  <q-item-label>{{grn.execAcc}}/{{grn.inDate}}</q-item-label>
  <q-item-label caption>{{grn.cmt}}</q-item-label>
 </q-item-section>
 <q-item-section side>{{grn.outDate}}</q-item-section>
</q-item>
</q-list>
</div>
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
    <q-input v-model.number="skuCtrl.dta.num" :label="tags.num" type="number"></q-input>
  </q-card-section>
  <q-card-actions align="right">
    <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    <q-btn :label="tags.ok" color="primary" @click="add_sku"></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="grnCtrl.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{tags.add}} {{tags.storage.in}}</div>
    <q-separator></q-separator>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <pur-select v-model="purchase" :label="tags.storage.purchase" v-show="grnCtrl.no<0"></pur-select>
   <q-input v-model="grnCtrl.dta.tranNo" :label="tags.storage.tranNo" dense></q-input>
   <date-input v-model="grnCtrl.dta.outDate" :close="tags.ok" :label="tags.storage.outDate" min="-5"></date-input>
   <q-input :label="tags.cmt" v-model="grnCtrl.dta.cmt" dense></q-input>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn :label="tags.remove" color="red" @click="remove_grn" flat v-show="grnCtrl.no>-1"></q-btn>
   <q-btn :label="tags.ok" color="primary" @click="grn_do"></q-btn>
   <q-btn :label="tags.close" color="primary" v-close-popup flat></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<q-dialog v-model="gdnCtrl.dlg">
 <q-card style="min-width:70vw">
  <q-card-section>
    <div class="text-h6">{{tags.add}} {{tags.storage.out}}</div>
    <q-separator></q-separator>
  </q-card-section>
  <q-card-section class="q-pt-none">
   <pur-select v-model="purchase" :label="tags.storage.purchase" v-show="gdnCtrl.no<0"></pur-select>
   <q-input v-model="gdnCtrl.dta.tranNo" :label="tags.storage.tranNo" dense>
    <template v-slot:append>
     <q-icon name="wb_auto" color="primary" @click="gen_gdnTranNo"></q-icon>
    </template>
   </q-input>
   <q-input :label="tags.cmt" v-model="gdnCtrl.dta.cmt" dense></q-input>
  </q-card-section>
  <q-card-actions align="right">
   <q-btn :label="tags.remove" color="red" @click="remove_gdn" flat v-show="gdnCtrl.no>-1"></q-btn>
   <q-btn :label="tags.ok" color="primary" @click="gdn_do"></q-btn>
   <q-btn :label="tags.close" color="primary" v-close-popup flat></q-btn>
  </q-card-actions>
 </q-card>
</q-dialog>

<!-- 申请支付弹窗 -->
<q-dialog v-model="payCtrl.dlg" no-backdrop-dismiss>
  <q-card style="min-width:70vw">
    <q-card-section>
      <div class="text-h6">{{tags.purchase.pay}}</div>
      <q-separator></q-separator>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <q-list>
      <q-item><q-item-section>
       <bank-select :label="tags.purchase.bank" v-model="payCtrl.dta.bank" dense></bank-select>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <date-input v-model="payCtrl.dta.expectAt" :format="tags.dateFmt"
       :label="tags.expDate" min="today"></date-input>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input :label="tags.cmt" v-model="payCtrl.dta.cmt" dense></q-input>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.ok" color="primary" @click="pay_do"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>

<alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></alert-dialog>
<confirm-dialog :title="tags.attention" :ok="tags.ok"
 :close="tags.cancel" ref="cfmDlg"></confirm-dialog>
`
}