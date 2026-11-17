import OrderDlg from "./orderdlg.js"

export default {
components:{
    "order-dlg":OrderDlg
},
inject:['service', 'tags'],
data() {return {
    state:'ALL',
    stateOpts:[],
    role:'',
    orders:[], //订单列表
    ctrl:{cur:1,max:0,onlyMine:false},
    score:{nOrder:0,vOrder:0,vBrokerage:0,total:0},
    alertDlg:null,
    confirmDlg:null
}},
created(){
    this.stateOpts=Object.entries(this.tags.order.states).map(
        ([k, v]) => {return {label:v, value:k}});

    this.service.getRole().then(role=>{
        this.role=role;
        this.query(1);
    })
},
mounted(){//不能在created中赋值，更不能在data中
    this.alertDlg=this.$refs.errMsg;
    this.confirmDlg=this.$refs.confirmDlg;    
},
methods:{
query(pg) {
    var offset=(parseInt(pg)-1)*this.service.NUM_PER_PAGE;
    var url=this.role=='admin'&&!this.ctrl.onlyMine?"/order/listAll":"/order/my";
    url+="?offset="+offset+"&num="+this.service.NUM_PER_PAGE+"&state="+this.state;
    request({method:"GET",url:url}, this.service.name).then(resp=>{
        if(resp.code!=RetCode.OK) {
            this.orders=[];
            this.ctrl.max=0;
        } else {
            this.score.total=resp.data.total;
            this.score.nOrder=resp.data.nOrder;
            this.score.vOrder=resp.data.vOrder;
            this.score.vBrokerage=resp.data.vBrokerage;
            this.formatData(resp.data.list, resp.data.cols);
            this.ctrl.max=Math.ceil(resp.data.total/this.service.NUM_PER_PAGE);
        }
    })
},
formatData(rows,cols) {
    var dt=new Date();
    this.orders=rows.map(l=>{
        var r={};
        for(var i in cols) {
            r[cols[i]]=l[i];
        }
        dt.setTime(r.createAt*60000);
        r.createAt=datetime2str(dt);
        r.state_s=this.tags.order.states[r.state];
        return r;
    })
},
show_order(id) {
    this.$refs.orderDlg.show(id);
},
refresh() {
    this.query(this.ctrl.cur)
}
},

template:`
<q-layout view="hHh lpr fFf">
  <q-header class="bg-grey-1 text-primary">
   <q-toolbar>
    <q-btn flat round icon="arrow_back" dense @click="service.back"></q-btn>
    <q-toolbar-title>{{tags.order.title}}</q-toolbar-title>
    <q-btn icon="refresh" flat dense @click="refresh"></q-btn>
    <q-btn flat round dense icon="menu"><q-menu>
     <div v-if="role=='admin'">
      <q-checkbox v-model="ctrl.onlyMine" :label="tags.onlyMine"
       @update:model-value="query(1)"></q-checkbox>
      <q-separator></q-separator>
     </div>
     <q-option-group :options="stateOpts" type="radio" v-model="state"
      @update:model-value="query(1)" style="min-width:10em"></q-option-group>
    </q-menu></q-btn>
   </q-toolbar>
   <q-card class="q-mx-sm" flat>
    <q-card-action>
    <q-markup-table flat dark dense style="background:radial-gradient(circle,#33a2ff 0%,#014aaa 100%)">
     <tr>
      <th>{{tags.score.total}}</th>
      <th>{{tags.score.nOrder}}</th>
      <th>{{tags.score.vOrder}}</th>
      <th>{{tags.score.vBrokerage}}</th>
     </tr>
     <tr>
      <td class="text-h6 text-center">{{score.total}}</td>
      <td class="text-h6 text-center">{{score.nOrder}}</td>
      <td class="text-h6 text-center">{{score.vOrder}}</td>
      <td class="text-h6 text-center">{{score.vBrokerage}}</td>
     </tr>
    </q-markup-table>
    </q-card-section>
   </q-card>
  </q-header>

  <q-page-container>
    <q-page class="q-pa-md">

<div class="q-pa-lg flex flex-center" v-if="ctrl.max>1">
 <q-pagination v-model="ctrl.cur" color="primary" :max="ctrl.max" max-pages="10"
  boundary-numbers="false" @update:model-value="query"></q-pagination>
</div>
<q-markup-table flat>
 <thead><tr>
  <th class="text-left">{{tags.vip.name}}</th>
  <th class="text-right">{{tags.order.val}}</th>
  <th class="text-right">{{tags.creator}}</th>
 </tr></thead>
 <tbody>
 <tr v-for="v in orders" style="cursor:pointer;" @click="show_order(v.id)">
  <td class="text-left">
   <div>{{v.name}}</div>
   <div class="text-caption">{{v.code}}</div>
  </td>
  <td class="text-right">
   <div>{{v.val}}</div>
   <div :class="v.state=='OK'?'text-caption':'text-primary'">{{v.state_s}}</div>
  </td>
  <td class="text-right">
   <div>{{v.creator}}</div>
   <div class="text-caption">{{v.createAt}}</div>
  </td>
 </tr>
 </tbody>
</q-markup-table>
    </q-page>
  </q-page-container>
</q-layout>

<order-dlg :tags="tags" :alertDlg="alertDlg" :confirmDlg="confirmDlg" :role="role" @done="refresh" ref="orderDlg"></order-dlg>
<component-confirm-dialog :title="tags.alert" :close="tags.cancel" :ok="tags.ok" ref="confirmDlg"></component-confirm-dialog>
<component-alert-dialog :title="tags.failToCall" :errMsgs="tags.errMsgs" ref="errMsg"></component-alert-dialog>
`
}